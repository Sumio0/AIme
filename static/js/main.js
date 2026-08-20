document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const messageInput = document.getElementById('message-input');
    const messagesContainer = document.getElementById('messages');
    const newChatBtn = document.querySelector('.new-chat-btn');
    const welcomeScreen = document.getElementById('welcome-screen');

    let chatHistory = [];
    let currentMbtiType = '';
    let mbtiData = {};
    
    // 初始化时加载所有MBTI数据
    fetch('/api/mbti')
        .then(response => response.json())
        .then(data => {
            mbtiData = data;
            
            // 随机选择一个MBTI类型的问候语，用于初始欢迎消息
            const mbtiTypes = Object.keys(mbtiData);
            const randomType = mbtiTypes[Math.floor(Math.random() * mbtiTypes.length)];
            
            // 如果欢迎屏幕存在，则替换标准欢迎文本为MBTI风格问候语
            if (welcomeScreen) {
                const greeting = mbtiData[randomType].greeting || '你好！我是AIme，有什么我可以帮助你的吗？';
                welcomeScreen.innerHTML = `
                    <h1>Welcome to AIME</h1>
                    <p>${greeting}</p>
                    <div style="margin-top: 16px;">
                        <button onclick="chooseOption('school')" style="margin-right: 12px;" class="lang-button">Apply to an Overseas School</button>
                        <button onclick="chooseOption('job')" class="lang-button">Help with Resume</button>
                    </div>
                `;
            }
        })
        .catch(err => {
            console.error('Failed to load MBTI data:', err);
        });

    // Auto-resize textarea
    messageInput.addEventListener('input', () => {
        messageInput.style.height = 'auto';
        messageInput.style.height = messageInput.scrollHeight + 'px';
    });

    // Handle form submission
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const message = messageInput.value.trim();
        if (!message) return;

        // 判断是否为MBTI类型
        const mbtiTypes = [
          "INFP","INFJ","ENFP","ENTP","INTJ","INTP","ENTJ","ENFJ",
          "ISFJ","ISTJ","ESFJ","ESTJ","ISFP","ISTP","ESFP","ESTP"
        ];
        
        // 检查消息是否是MBTI类型
        if (mbtiTypes.includes(message.toUpperCase())) {
            currentMbtiType = message.toUpperCase();
            addMessage('user', message);
            handleMBTIInput(message);
            messageInput.value = '';
            messageInput.style.height = 'auto';
            return;
        }

        // Add user message
        addMessage('user', message);
        messageInput.value = '';
        messageInput.style.height = 'auto';

        // Show typing indicator
        const typingIndicator = showTypingIndicator();

        try {
            // Call API
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: message
                })
            });

            const data = await response.json();
            
            // Remove typing indicator
            typingIndicator.remove();

            // Add AI response
            const aiResponse = data.response || "Sorry, I couldn't process that.";
            addMessage('assistant', aiResponse);

            // Save to chat history
            chatHistory.push(
                { role: 'user', content: message },
                { role: 'assistant', content: aiResponse }
            );

            // Scroll to bottom
            scrollToBottom();

        } catch (error) {
            console.error('Error:', error);
            typingIndicator.remove();
            
            let errorMessage = 'Sorry, there was an error processing your request.';
            
            if (error.message) {
                errorMessage += ' (' + error.message + ')';
                console.log('Error details:', error.message);
            }
            
            addMessage('assistant', errorMessage);
        }
    });

    // Handle Enter key
    messageInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            chatForm.dispatchEvent(new Event('submit'));
        }
    });

    // New chat button
    newChatBtn.addEventListener('click', () => {
        chatHistory = [];
        currentMbtiType = '';
        
        // 随机选择一个MBTI类型的问候语
        const mbtiTypes = Object.keys(mbtiData);
        const randomType = mbtiTypes[Math.floor(Math.random() * mbtiTypes.length)];
        const greeting = mbtiData[randomType].greeting || '你好！我是AIme，有什么我可以帮助你的吗？';
        
        messagesContainer.innerHTML = `
            <div class="welcome-screen">
                <h1>Welcome to AIME</h1>
                <p>${greeting}</p>
                <div style="margin-top: 16px;">
                    <button onclick="chooseOption('school')" style="margin-right: 12px;" class="lang-button">Apply to an Overseas School</button>
                    <button onclick="chooseOption('job')" class="lang-button">Help with Resume</button>
                </div>
            </div>
        `;
    });

    // Load MBTI data if user input is a personality type
    function handleMBTIInput(mbti) {
        fetch(`/api/mbti?type=${mbti.toUpperCase()}`)
            .then(res => res.json())
            .then(data => {
                if (data && !data.error) {
                    const upperType = mbti.toUpperCase();
                    let response = `你是一个${upperType}类型的人！\n\n特点：${data.strength}\n\n建议：${data.recommendation}`;
                    
                    // 添加定制问候语
                    if (data.greeting) {
                        response += `\n\n作为AI助手，我会尽量以更适合你的方式提供帮助:\n${data.greeting}`;
                    }
                    
                    addMessage('assistant', response);
                    chatHistory.push(
                        { role: 'user', content: mbti },
                        { role: 'assistant', content: response }
                    );
                    scrollToBottom();
                } else {
                    addMessage('assistant', '抱歉，我无法识别这个MBTI类型。');
                }
            })
            .catch(err => {
                console.error('获取MBTI数据失败:', err);
                addMessage('assistant', '获取MBTI信息时出错，请稍后再试。');
            });
    }

    // Helper functions
    function addMessage(role, content) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${role === 'assistant' ? 'ai-message' : 'user-message'}`;
        messageDiv.textContent = content;
        
        // Remove welcome screen if present
        const welcomeScreen = messagesContainer.querySelector('.welcome-screen');
        if (welcomeScreen) {
            welcomeScreen.remove();
        }

        messagesContainer.appendChild(messageDiv);
        scrollToBottom();
    }

    function showTypingIndicator() {
        const indicator = document.createElement('div');
        indicator.className = 'typing-indicator';
        indicator.innerHTML = `
            <div class="typing-circle"></div>
            <div class="typing-circle"></div>
            <div class="typing-circle"></div>
        `;
        messagesContainer.appendChild(indicator);
        scrollToBottom();
        return indicator;
    }

    function scrollToBottom() {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
});

// 处理选择海外学校申请或求职帮助的选项
function chooseOption(option) {
    const messages = document.getElementById("messages");
    const welcomeScreen = document.getElementById("welcome-screen");
    
    if (welcomeScreen) {
        welcomeScreen.remove();
    }
    
    if (option === 'school') {
        // 首先询问MBTI类型
        messages.innerHTML += `
            <div class="ai-message">
                <p>申请海外学校是一个重要的决定！为了给你提供更个性化的建议，我想先了解一下你的MBTI性格类型。</p>
                <p>请告诉我你的MBTI类型（例如INFP、ENTJ等）。如果你不知道自己的类型，可以简单回复"不知道"，我会给你提供一般性建议。</p>
            </div>
        `;
        
        // 添加一个事件监听器，处理用户输入的MBTI类型
        const messageInput = document.getElementById('message-input');
        const chatForm = document.getElementById('chat-form');
        
        const schoolOptionHandler = function(e) {
            e.preventDefault();
            const mbtiType = messageInput.value.trim().toUpperCase();
            
            // 添加用户消息
            messages.innerHTML += `
                <div class="user-message">${messageInput.value}</div>
            `;
            messageInput.value = '';
            
            // 有效的MBTI类型列表
            const validTypes = [
                "INFP","INFJ","ENFP","ENTP","INTJ","INTP","ENTJ","ENFJ",
                "ISFJ","ISTJ","ESFJ","ESTJ","ISFP","ISTP","ESFP","ESTP"
            ];
            
            if (validTypes.includes(mbtiType)) {
                // 获取特定MBTI类型的海外申请建议
                fetch(`/api/mbti?type=${mbtiType}`)
                    .then(res => res.json())
                    .then(data => {
                        if (data && data.overseas_application) {
                            messages.innerHTML += `
                                <div class="ai-message">
                                    <p>${data.overseas_application}</p>
                                    <p>接下来，你想了解哪些具体方面？比如申请材料准备、选校策略、面试技巧等？</p>
                                </div>
                            `;
                        } else {
                            // 默认回复
                            messages.innerHTML += `
                                <div class="ai-message">
                                    <p>谢谢分享你的MBTI类型！申请海外学校时，重要的是展示你的个人特质和优势。</p>
                                    <p>你有什么具体的问题或者想了解哪个国家的学校申请流程？</p>
                                </div>
                            `;
                        }
                        messages.scrollTop = messages.scrollHeight;
                    })
                    .catch(err => {
                        console.error('获取MBTI数据失败:', err);
                        // 发生错误时的默认响应
                        messages.innerHTML += `
                            <div class="ai-message">
                                <p>谢谢分享你的MBTI类型！申请海外学校时，重要的是展示你的个人特质和优势。</p>
                                <p>你有什么具体的问题或者想了解哪个国家的学校申请流程？</p>
                            </div>
                        `;
                        messages.scrollTop = messages.scrollHeight;
                    });
            } else if (mbtiType === "不知道" || mbtiType === "UNKNOWN" || mbtiType === "DON'T KNOW") {
                // 如果用户不知道自己的MBTI类型
                messages.innerHTML += `
                    <div class="ai-message">
                        <p>没关系！即使不知道MBTI类型，我们也可以开始海外学校申请的讨论。</p>
                        <p>一般来说，成功的申请需要展示你的学术能力、个人特质和明确的学习目标。</p>
                        <p>你对哪个国家或地区的学校感兴趣？或者你想了解申请流程中的哪个具体环节？</p>
                    </div>
                `;
            } else {
                // 如果输入的不是有效的MBTI类型或"不知道"
                messages.innerHTML += `
                    <div class="ai-message">
                        <p>似乎你输入的不是标准的MBTI类型。MBTI包括16种类型，如INFP、ENTJ等。</p>
                        <p>不过没关系，我们可以继续讨论海外学校申请。你对哪个国家或地区的学校感兴趣？</p>
                    </div>
                `;
            }
            
            messages.scrollTop = messages.scrollHeight;
            
            // 移除这个特殊的事件监听器，恢复正常的聊天流程
            chatForm.removeEventListener('submit', schoolOptionHandler);
        };
        
        chatForm.addEventListener('submit', schoolOptionHandler);
    } else if (option === 'job') {
        messages.innerHTML += `
            <div class="user-message"><p>I need help with my resume.</p></div>
            <div class="ai-message">
                <p>Sure! Please tell me what type of job you are applying for and any specific areas you'd like help with.</p>
            </div>
        `;
    }
    
    messages.scrollTop = messages.scrollHeight;
}
