/**
 * AIME - Global Language Switching
 * This file handles language switching across all pages.
 */

document.addEventListener('DOMContentLoaded', function() {
    // 检查URL中的lang参数
    const urlParams = new URLSearchParams(window.location.search);
    const langParam = urlParams.get('lang');
    
    // 从localStorage获取保存的语言，如果没有则默认为zh
    let currentLang = localStorage.getItem('lang') || 'zh';
    
    // 如果URL中有lang参数，则优先使用它并更新localStorage
    if (langParam && (langParam === 'en' || langParam === 'zh')) {
        currentLang = langParam;
        localStorage.setItem('lang', currentLang);
    }
    
    // 设置html的lang属性
    document.documentElement.setAttribute('lang', currentLang);
    
    // 更新所有带有data-i18n属性的元素文本
    updateI18nElements();
    
    // 更新语言切换按钮
    updateLangToggleBtn();
    
    // 为语言切换按钮添加点击事件
    const langToggleBtn = document.getElementById('lang-toggle');
    if (langToggleBtn) {
        langToggleBtn.addEventListener('click', toggleLanguage);
    }
    
    // 当点击语言切换按钮时
    function toggleLanguage() {
        // 切换语言
        currentLang = currentLang === 'en' ? 'zh' : 'en';
        
        // 保存语言选择到localStorage
        localStorage.setItem('lang', currentLang);
        
        // 更新html的lang属性
        document.documentElement.setAttribute('lang', currentLang);
        
        // 更新所有带有data-i18n属性的元素文本
        updateI18nElements();
        
        // 更新语言切换按钮
        updateLangToggleBtn();
        
        // 更新所有链接中的lang参数
        updateLinkParams();
    }
    
    // 更新所有链接的lang参数
    function updateLinkParams() {
        const links = document.getElementsByTagName('a');
        for (let i = 0; i < links.length; i++) {
            const link = links[i];
            
            // 只处理内部链接
            if (link.href.includes(window.location.hostname) || link.href.startsWith('/') || link.href.startsWith('./') || link.href.startsWith('../')) {
                try {
                    const url = new URL(link.href, window.location.origin);
                    url.searchParams.set('lang', currentLang);
                    link.href = url.toString();
                } catch (e) {
                    console.error("Error updating link:", link.href, e);
                }
            }
        }
    }
    
    // 初始化更新所有链接的lang参数
    updateLinkParams();
    
    // 更新所有带有data-i18n属性的元素文本
    function updateI18nElements() {
        const i18nElements = document.querySelectorAll('[data-i18n]');
        i18nElements.forEach(el => {
            const key = el.getAttribute('data-i18n');
            if (window.AIME_TRANSLATIONS && 
                window.AIME_TRANSLATIONS[currentLang] && 
                window.AIME_TRANSLATIONS[currentLang][key]) {
                el.textContent = window.AIME_TRANSLATIONS[currentLang][key];
            }
        });
    }
    
    // 更新语言切换按钮
    function updateLangToggleBtn() {
        const langToggleBtn = document.getElementById('lang-toggle');
        if (langToggleBtn) {
            langToggleBtn.textContent = currentLang === 'en' ? 'EN / 中文' : '中文 / EN';
        }
    }
}); 