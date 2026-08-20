// Text to speech functionality using Google Cloud Text-to-Speech API
const GOOGLE_TTS_API_KEY = "AIzaSyAnRx8aEinsjb_ZLkegVVZoP8U-Eo6m2NE";

function speakText(text) {
    // Create the request body
    const requestBody = {
        input: { text: text },
        voice: {
            languageCode: "en-US",
            name: "en-US-Neural2-D",
            ssmlGender: "MALE"
        },
        audioConfig: {
            audioEncoding: "MP3",
            speakingRate: 1.0,
            pitch: 0
        }
    };

    // Make the API request
    fetch(`https://texttospeech.googleapis.com/v1/text:synthesize?key=${GOOGLE_TTS_API_KEY}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(requestBody)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.audioContent) {
            // Convert base64 to audio
            const audioContent = data.audioContent;
            const audioBlob = new Blob(
                [Uint8Array.from(atob(audioContent), c => c.charCodeAt(0))],
                { type: 'audio/mp3' }
            );
            const audioUrl = URL.createObjectURL(audioBlob);
            const audio = new Audio(audioUrl);
            
            // Play the audio
            audio.oncanplaythrough = () => {
                audio.play().catch(error => {
                    console.error("Error playing audio:", error);
                });
            };
            
            // Clean up the URL after playing
            audio.onended = () => {
                URL.revokeObjectURL(audioUrl);
            };
        } else {
            console.error("No audio content received from Google TTS API");
        }
    })
    .catch(error => {
        console.error("Error with Google TTS API:", error);
        alert("Error generating speech. Please check the console for details.");
    });
} 