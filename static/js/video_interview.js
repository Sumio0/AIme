// Resume Upload and Interview Question Generation
document.addEventListener('DOMContentLoaded', function() {
    const resumeUpload = document.getElementById('resume-upload');
    const interviewSetup = document.getElementById('interview-setup');
    const uploadResumeBtn = document.getElementById('upload-resume');
    const resumeFile = document.getElementById('resume-file');
    const resumeText = document.getElementById('resume-text');
    const userVideo = document.getElementById('user-video');
    const recordingIndicator = document.getElementById('recording-indicator');
    
    let mediaRecorder;
    let recordedChunks = [];
    
    // Initially hide interview setup
    if (interviewSetup) {
        interviewSetup.style.display = 'none';
    }
    
    // Function to start video recording
    async function startRecording() {
        try {
            // Request both video and audio permissions
            const stream = await navigator.mediaDevices.getUserMedia({
                video: {
                    width: { ideal: 1280 },
                    height: { ideal: 720 }
                },
                audio: {
                    echoCancellation: true,
                    noiseSuppression: true,
                    autoGainControl: true
                }
            });
            
            // Set video source and ensure audio is enabled
            userVideo.srcObject = stream;
            userVideo.muted = false; // Ensure audio is not muted
            
            // Create MediaRecorder with audio support
            const options = {
                mimeType: 'video/webm;codecs=vp9,opus',
                audioBitsPerSecond: 128000,
                videoBitsPerSecond: 2500000
            };
            
            try {
                mediaRecorder = new MediaRecorder(stream, options);
            } catch (e) {
                console.warn('Preferred MIME type not supported, falling back to default');
                mediaRecorder = new MediaRecorder(stream);
            }
            
            // Handle data available event
            mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    recordedChunks.push(event.data);
                }
            };
            
            // Handle recording stop
            mediaRecorder.onstop = () => {
                const blob = new Blob(recordedChunks, {
                    type: 'video/webm'
                });
                const url = URL.createObjectURL(blob);
                
                // Create download link
                const a = document.createElement('a');
                a.href = url;
                a.download = `interview-recording-${new Date().toISOString()}.webm`;
                a.click();
                
                // Clean up
                URL.revokeObjectURL(url);
                recordedChunks = [];
            };
            
            // Start recording
            mediaRecorder.start(1000); // Collect data every second
            recordingIndicator.style.display = 'block';
            
            // Set up timer for recording
            let recordingTime = 0;
            const timerInterval = setInterval(() => {
                recordingTime++;
                const minutes = Math.floor(recordingTime / 60);
                const seconds = recordingTime % 60;
                document.getElementById('timer-display').textContent = 
                    `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
            }, 1000);
            
            // Stop recording after 5 minutes
            setTimeout(() => {
                stopRecording();
                clearInterval(timerInterval);
            }, 5 * 60 * 1000);
            
        } catch (error) {
            console.error('Error accessing media devices:', error);
            alert('Error accessing camera and microphone. Please make sure you have granted the necessary permissions.');
        }
    }
    
    // Function to stop recording
    function stopRecording() {
        if (mediaRecorder && mediaRecorder.state !== 'inactive') {
            mediaRecorder.stop();
            recordingIndicator.style.display = 'none';
            
            // Stop all tracks
            const stream = userVideo.srcObject;
            if (stream) {
                stream.getTracks().forEach(track => track.stop());
            }
        }
    }
    
    // Handle resume upload
    uploadResumeBtn.addEventListener('click', async function() {
        const formData = new FormData();
        
        // Check if file is uploaded
        if (resumeFile.files.length > 0) {
            formData.append('resume_file', resumeFile.files[0]);
        }
        
        // Check if text is entered
        if (resumeText.value.trim()) {
            formData.append('resume_text', resumeText.value.trim());
        }
        
        if (formData.has('resume_file') || formData.has('resume_text')) {
            try {
                const response = await fetch('/api/upload-resume', {
                    method: 'POST',
                    body: formData
                });
                
                if (response.ok) {
                    const data = await response.json();
                    // Store resume data in localStorage for later use
                    localStorage.setItem('resumeData', JSON.stringify(data));
                    
                    // Show interview setup
                    resumeUpload.style.display = 'none';
                    interviewSetup.style.display = 'block';
                } else {
                    alert('Failed to upload resume. Please try again.');
                }
            } catch (error) {
                console.error('Error uploading resume:', error);
                alert('An error occurred while uploading your resume. Please try again.');
            }
        } else {
            alert('Please either upload a resume file or paste your resume text.');
        }
    });
    
    // Modify the start interview button click handler
    const startInterviewBtn = document.getElementById('start-interview');
    if (startInterviewBtn) {
        startInterviewBtn.addEventListener('click', async function() {
            const candidateName = document.getElementById('candidate-name').value;
            const jobPosition = document.getElementById('job-position').value;
            const interviewType = document.getElementById('interview-type').value;
            
            // Get stored resume data
            const resumeData = JSON.parse(localStorage.getItem('resumeData') || '{}');
            
            try {
                // Generate interview questions based on resume and job position
                const response = await fetch('/api/generate-questions', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        candidate_name: candidateName,
                        job_position: jobPosition,
                        interview_type: interviewType,
                        resume_data: resumeData
                    })
                });
                
                if (response.ok) {
                    const data = await response.json();
                    // Store questions in localStorage
                    localStorage.setItem('interviewQuestions', JSON.stringify(data.questions));
                    
                    // Start the interview
                    startInterview();
                } else {
                    alert('Failed to generate interview questions. Please try again.');
                }
            } catch (error) {
                console.error('Error generating questions:', error);
                alert('An error occurred while generating interview questions. Please try again.');
            }
        });
    }
    
    // Function to start the interview
    function startInterview() {
        const interviewSetup = document.getElementById('interview-setup');
        const interviewRecording = document.getElementById('interview-recording');
        
        if (interviewSetup && interviewRecording) {
            interviewSetup.style.display = 'none';
            interviewRecording.style.display = 'block';
            
            // Initialize the interview with the first question
            const questions = JSON.parse(localStorage.getItem('interviewQuestions') || '[]');
            if (questions.length > 0) {
                document.getElementById('current-question').textContent = questions[0];
            }
            
            // Start video recording
            startRecording();
        }
    }
}); 