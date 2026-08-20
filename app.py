from flask import Flask, render_template, request, jsonify, url_for, flash, redirect
import os
import json
import openai
from dotenv import load_dotenv
import requests  # Add requests library for calling Claude API
import argparse
import time
import random
import datetime
import traceback
import re

# Load environment variables
load_dotenv()

# Configure Claude API key
openai_api_key = os.getenv("OPENAI_API_KEY")
# Directly configure Claude API key
claude_api_key = os.getenv("CLAUDE_API_KEY")

if openai_api_key:
    openai.api_key = openai_api_key
    print("OpenAI API key configured")
elif claude_api_key:
    print("Claude API key configured")
else:
    print("Warning: No OpenAI or Claude API key found. Will use mock data.")

# Get the absolute path of the directory containing this file
basedir = os.path.abspath(os.path.dirname(__file__))
# Define the absolute paths to the template and static folders
template_dir = os.path.join(basedir, 'templates')
static_dir = os.path.join(basedir, 'static')

app = Flask(__name__, 
            template_folder=template_dir,
            static_folder=static_dir)

# Configure upload folder
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'temp_uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Set key for session and flash messages
app.secret_key = os.environ.get('SECRET_KEY', 'aime_development_secret_key')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/community")
def community():
    return render_template("community.html")

@app.route("/careers")
def careers():
    return render_template("careers.html")

@app.route("/exchange")
def exchange():
    # Deprecated: Exchange program feature is temporarily disabled.
    return redirect(url_for('index'))

@app.route("/gap")
def gap():
    return render_template("gap.html")

@app.route("/startup")
def startup():
    return render_template("startup.html")

@app.route("/video-interview")
def video_interview():
    return render_template("video_interview.html")

@app.route("/project-form")
def project_form():
    return render_template("project_form.html")

@app.route("/resume-form")
def resume_form():
    return render_template("resume_form.html")

@app.route("/founder-form")
def founder_form():
    return render_template("founder_form.html")

@app.route("/submit-project", methods=["POST"])
def submit_project():
    """Handle startup project form submission"""
    try:
        # Get form data
        project_name = request.form.get('project_name')
        project_stage = request.form.get('project_stage')
        project_summary = request.form.get('project_summary')
        project_description = request.form.get('project_description')
        project_country = request.form.get('project_country')
        project_city = request.form.get('project_city', '')
        project_tags = request.form.getlist('project_tags')
        project_seeking = request.form.get('project_seeking')
        
        # Get founder information
        founder_name = request.form.get('founder_name')
        founder_email = request.form.get('founder_email')
        founder_wechat = request.form.get('founder_wechat', '')
        
        # Get options
        public_contact = 'yes' if request.form.get('public_contact') == 'yes' else 'no'
        agree_terms = request.form.get('agree_terms')
        
        # Handle image upload
        project_image = None
        if 'project_image' in request.files and request.files['project_image'].filename != '':
            image_file = request.files['project_image']
            # In a real project, the image should be saved to server or cloud storage
            # For now, we just get the filename to demonstrate functionality
            project_image = image_file.filename
        
        # TODO: Save data to database
        # In a real project, you should:
        # 1. Validate data
        # 2. Save images to appropriate storage
        # 3. Save records to database
        
        # Temporarily simulate successful processing and return to startup center
        # In actual implementation, should also return success message or error handling
        
        # Use flash message to notify user of successful submission
        flash('Your startup project has been successfully submitted, we will review it soon!', 'success')
        
        return redirect(url_for('startup'))
        
    except Exception as e:
        # Log error and display to user
        print(f"Project submission error: {e}")
        flash('An error occurred during submission, please try again later.', 'error')
        return redirect(url_for('project_form'))

@app.route("/submit-founder", methods=["POST"])
def submit_founder():
    """Handle co-founder form submission"""
    try:
        # Get form data
        founder_name = request.form.get('founder_name')
        founder_title = request.form.get('founder_title')
        founder_experience = request.form.get('founder_experience')
        founder_bio = request.form.get('founder_bio')
        founder_previous = request.form.get('founder_previous', '')
        founder_skills = request.form.getlist('founder_skills')
        founder_interests = request.form.getlist('founder_interests')
        founder_email = request.form.get('founder_email')
        founder_social = request.form.get('founder_social', '')
        founder_seeking = request.form.get('founder_seeking')
        
        # Get options
        has_project = 'yes' if request.form.get('has_project') == 'yes' else 'no'
        public_contact = 'yes' if request.form.get('public_contact') == 'yes' else 'no'
        agree_terms = request.form.get('agree_terms')
        
        # Handle image upload
        founder_photo = None
        if 'founder_photo' in request.files and request.files['founder_photo'].filename != '':
            photo_file = request.files['founder_photo']
            # In a real project, the image should be saved to server or cloud storage
            # For now, we just get the filename to demonstrate functionality
            founder_photo = photo_file.filename
        
        # TODO: Save data to database
        # In a real project, you should:
        # 1. Validate data
        # 2. Save images to appropriate storage
        # 3. Save records to database
        
        # Temporarily simulate successful processing and return to startup center
        # In actual implementation, should also return success message or error handling
        
        # Use flash message to notify user of successful submission
        flash('Your founder profile has been successfully submitted and will be displayed in the co-founder search section!', 'success')
        
        return redirect(url_for('startup'))
        
    except Exception as e:
        # Log error and display to user
        print(f"Founder profile submission error: {e}")
        flash('An error occurred during submission, please try again later.', 'error')
        return redirect(url_for('founder_form'))

@app.route("/submit-resume", methods=["POST"])
def submit_resume():
    """Handle resume form submission"""
    try:
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        location = request.form.get('location')
        summary = request.form.get('summary')
        experience = request.form.get('experience')
        education = request.form.get('education')
        skills = request.form.get('skills')
        template = request.form.get('template')
        
        # TODO: Generate resume PDF
        # In a real project, you should:
        # 1. Validate data
        # 2. Generate PDF using a library like reportlab or weasyprint
        # 3. Save PDF to server or cloud storage
        # 4. Return PDF URL to user
        
        # For now, just return success message
        flash('Your resume has been successfully generated!', 'success')
        return redirect(url_for('careers'))
        
    except Exception as e:
        # Log error and display to user
        print(f"Resume generation error: {e}")
        flash('An error occurred during resume generation, please try again later.', 'error')
        return redirect(url_for('resume_form'))

@app.route("/api/analyze-interview", methods=["POST"])
def analyze_interview():
    """Receive interview transcript and return analysis results"""
    if not request.json:
        return jsonify({"error": "No data provided"}), 400
    
    # Support two formats: 1. Old version pure text transcript 2. New version structured qa_pairs
    transcript = request.json.get('transcript', '')
    job_position = request.json.get('job_position', 'Unspecified position')
    candidate_name = request.json.get('candidate_name', 'Unspecified name')
    qa_pairs = request.json.get('qa_pairs', [])
    language = request.json.get('language', 'en')  # Get language parameter, default English
    
    # If qa_pairs provided, convert to text format for analysis
    if qa_pairs and not transcript:
        transcript = ""
        for qa in qa_pairs:
            lang_key = qa.get('language', language)
            question_prefix = "Question: " if lang_key == "zh" else "Question: "
            answer_prefix = "Answer: " if lang_key == "zh" else "Answer: "
            
            transcript += f"{question_prefix}{qa.get('question', '')}\n"
            transcript += f"{answer_prefix}{qa.get('answer', '')}\n\n"
    
    # Ensure there is content to analyze
    if not transcript:
        return jsonify({"error": "No transcript or QA pairs provided"}), 400
    
    # First try using OpenAI API
    if openai_api_key:
        try:
            analysis = analyze_with_openai(transcript, job_position, candidate_name, language)
            return jsonify(analysis)
        except Exception as e:
            print(f"OpenAI API call error: {e}")
            # If OpenAI API call fails, try using Claude API
            if claude_api_key:
                try:
                    analysis = analyze_with_claude(transcript, job_position, candidate_name, language)
                    return jsonify(analysis)
                except Exception as e:
                    print(f"Claude API call error: {e}")
                    analysis = generate_mock_analysis(transcript, job_position, candidate_name, language)
                    return jsonify(analysis)
            else:
                # No Claude API key, use mock data
                analysis = generate_mock_analysis(transcript, job_position, candidate_name, language)
                return jsonify(analysis)
    # Try using Claude API
    elif claude_api_key:
        try:
            analysis = analyze_with_claude(transcript, job_position, candidate_name, language)
            return jsonify(analysis)
        except Exception as e:
            print(f"Claude API call error: {e}")
            # Claude API call fails, use mock data
            analysis = generate_mock_analysis(transcript, job_position, candidate_name, language)
            return jsonify(analysis)
    else:
        # No API keys, use mock data
        analysis = generate_mock_analysis(transcript, job_position, candidate_name, language)
        return jsonify(analysis)

@app.route("/api/transcribe", methods=["POST"])
def transcribe_audio():
    """Convert audio to text (API endpoint)"""
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400
    
    audio_file = request.files['audio']
    
    # Save temporary file
    temp_filename = "temp_audio.webm"
    audio_file.save(temp_filename)
    
    try:
        # First try using OpenAI API
        if openai_api_key:
            try:
                client = openai.OpenAI()
                with open(temp_filename, "rb") as audio_file:
                    transcript = client.audio.transcriptions.create(
                        model="whisper-1", 
                        file=audio_file,
                        language="en"  # Default to English
                    )
                text = transcript.text
                return jsonify({"transcript": text})
            except Exception as e:
                print(f"Whisper API error: {e}")
                # Return mock data if failed
                return jsonify({"transcript": "This is a mock transcript text because the speech recognition API call failed."})
        else:
            # Return mock data if no API key
            return jsonify({"transcript": "This is a mock transcript text because no speech recognition API key is configured."})
    finally:
        # Clean up temporary file
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

@app.route("/api/set-api-keys", methods=["POST"])
def set_api_keys():
    """Set API keys (received from frontend)"""
    if 'openai_api_key' in request.json:
        openai_api_key = request.json['openai_api_key']
        if openai_api_key:
            openai.api_key = openai_api_key
            return jsonify({"success": True, "message": "OpenAI API key has been set"})
    
    if 'claude_api_key' in request.json:
        global claude_api_key
        claude_api_key = request.json['claude_api_key']
        if claude_api_key:
            return jsonify({"success": True, "message": "Claude API key has been set"})
    
    return jsonify({"success": False, "message": "No API key provided"})

@app.route("/api/chat", methods=["POST"])
def chat_api():
    if 'message' not in request.json:
        return jsonify({"error": "No message provided"}), 400
    message = request.json['message']
    ai_api_key = request.json.get('ai_api_key') or os.getenv('DEEPSEEK_API_KEY')

    # If DeepSeek API key is provided, use DeepSeek
    if ai_api_key:
        try:
            response = chat_with_deepseek(message, ai_api_key)
            return jsonify({"response": response})
        except Exception as e:
            print(f"DeepSeek API error: {e}")
            return jsonify({"error": f"Error calling DeepSeek API: {str(e)}"}), 500
    # If Claude API configured, use Claude for chat
    elif claude_api_key:
        try:
            response = chat_with_claude(message)
            return jsonify({"response": response})
        except Exception as e:
            print(f"Claude API error: {e}")
            return jsonify({"error": f"Error calling Claude API: {str(e)}"}), 500
    # If OpenAI API configured, use OpenAI for chat
    elif openai_api_key:
        try:
            response = chat_with_openai(message)
            return jsonify({"response": response})
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return jsonify({"error": f"Error calling OpenAI API: {str(e)}"}), 500
    else:
        # No API keys, return mock response
        return jsonify({"response": "I am a mock AI assistant. Since no API key is configured, I can only provide this preset response."})

def chat_with_claude(message):
    """Chat with Claude API"""
    headers = {
        "x-api-key": claude_api_key,
        "Content-Type": "application/json"
    }
    
    data = {
        "messages": [
            {
                "role": "user",
                "content": message
            }
        ],
        "model": "claude-3-opus-20240229",
        "max_tokens": 1000
    }
    
    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers=headers,
        json=data
    )
    
    if response.status_code == 200:
        return response.json()["content"][0]["text"]
    else:
        raise Exception(f"Claude API error: {response.text}")

def chat_with_openai(message):
    """Chat with OpenAI API"""
    client = openai.OpenAI()
    
    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant. Please respond in English only."},
            {"role": "user", "content": message}
        ],
        max_tokens=1000
    )
    
    return response.choices[0].message.content

def chat_with_deepseek(message, api_key):
    """Chat with DeepSeek API"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": message}
        ],
        "max_tokens": 1000
    }
    response = requests.post(
        "https://api.deepseek.com/v1/chat/completions",
        headers=headers,
        json=data
    )
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise Exception(f"DeepSeek API error: {response.text}")

@app.route("/api/mbti", methods=["GET"])
def get_mbti_data():
    """Get MBTI type data, including greetings and overseas application suggestions"""
    mbti_type = request.args.get('type', '').upper()
    
    try:
        # Read MBTI data file
        with open(os.path.join(static_dir, 'js/mbti_data.json'), 'r', encoding='utf-8') as f:
            mbti_data = json.load(f)
        
        if mbti_type and mbti_type in mbti_data:
            return jsonify(mbti_data[mbti_type])
        else:
            # If type not specified or doesn't exist, return all data
            return jsonify(mbti_data)
    
    except Exception as e:
        return jsonify({"error": f"Failed to get MBTI data: {str(e)}"}), 500

@app.route("/api/store-interview-data", methods=["POST"])
def store_interview_data():
    """Store interview data in backend, including questions, answers, and candidate information"""
    if not request.json:
        return jsonify({"error": "No interview data provided"}), 400
    
    interview_data = request.json
    
    try:
        # Ensure storage directory exists
        data_dir = os.path.join(basedir, 'data', 'interviews')
        os.makedirs(data_dir, exist_ok=True)
        
        # Create unique ID (timestamp + random number)
        timestamp = int(time.time())
        random_suffix = random.randint(1000, 9999)
        unique_id = f"{timestamp}-{random_suffix}"
        
        # Check data type: single QA pair vs complete interview data
        if 'question' in interview_data and 'answer' in interview_data:
            # Single QA pair
            required_fields = ['candidate_name', 'job_position', 'interview_type', 'question', 'answer']
            for field in required_fields:
                if field not in interview_data:
                    return jsonify({"error": f"Missing required field: {field}"}), 400
            
            # Format single QA pair
            qa_pair = {
                'candidate_name': interview_data['candidate_name'],
                'job_position': interview_data['job_position'],
                'interview_type': interview_data['interview_type'],
                'timestamp': interview_data.get('timestamp', datetime.datetime.now().isoformat()),
                'qa_pair': {
                    'question': interview_data['question'],
                    'answer': interview_data['answer']
                },
                'id': f"answer-{unique_id}"
            }
            
            # Output to console
            print(f"Received single QA pair: {json.dumps(qa_pair, ensure_ascii=False)}")
            
            # Save to file (ensure persistent storage)
            answer_id = qa_pair['id']
            filename = os.path.join(data_dir, f"answer-{answer_id}.json")
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(qa_pair, f, ensure_ascii=False, indent=2)
            
            # If needed, database storage code can be added here
            
            return jsonify({
                "success": True,
                "message": "QA pair successfully stored",
                "answer_id": answer_id
            })
            
        else:
            # Complete interview data
            required_fields = ['candidate_name', 'job_position', 'interview_type', 'qa_pairs']
            for field in required_fields:
                if field not in interview_data:
                    return jsonify({"error": f"Missing required field: {field}"}), 400
            
            # Ensure qa_pairs is a list
            if not isinstance(interview_data['qa_pairs'], list):
                return jsonify({"error": "Field qa_pairs must be an array"}), 400
            
            # Add timestamp (if not exists) and ID
            if 'timestamp' not in interview_data:
                interview_data['timestamp'] = datetime.datetime.now().isoformat()
            
            interview_id = f"interview-{unique_id}"
            interview_data['id'] = interview_id
            
            # Output to console
            print(f"Received complete interview data: {json.dumps(interview_data, ensure_ascii=False)[:200]}...")
            
            # Save to file (ensure persistent storage)
            filename = os.path.join(data_dir, f"interview-{interview_id}.json")
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(interview_data, f, ensure_ascii=False, indent=2)
            
            # If needed, you can add database storage logic here
            # For example: db.interviews.insert_one(interview_data)
            
            # Automatically call AI scoring API (if API key configured)
            if claude_api_key or openai_api_key:
                try:
                    # Build complete text from qa_pairs
                    transcript = ""
                    for qa in interview_data['qa_pairs']:
                        transcript += f"Question: {qa.get('question', '')}\n"
                        transcript += f"Answer: {qa.get('answer', '')}\n\n"
                    
                    # Call analysis interface
                    if claude_api_key:
                        print(f"Using Claude API to analyze interview data...")
                        analysis = analyze_with_claude(
                            transcript, 
                            interview_data['job_position'], 
                            interview_data['candidate_name']
                        )
                    else:
                        print(f"Using OpenAI API to analyze interview data...")
                        analysis = analyze_with_openai(
                            transcript, 
                            interview_data['job_position'], 
                            interview_data['candidate_name']
                        )
                    
                    # Add analysis results to interview data
                    interview_data['analysis'] = analysis
                    
                    # Update file
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(interview_data, f, ensure_ascii=False, indent=2)
                    
                    # Return result with analysis
                    return jsonify({
                        "success": True, 
                        "message": "Interview data successfully stored and analyzed",
                        "interview_id": interview_id,
                        "analysis": analysis
                    })
                    
                except Exception as e:
                    print(f"Automatic analysis failed: {str(e)}")
                    traceback.print_exc()  # Print complete error stack
            
            # If no API key configured or analysis failed, return basic success message
            return jsonify({
                "success": True, 
                "message": "Interview data successfully stored",
                "interview_id": interview_id
            })
        
    except Exception as e:
        print(f"Error storing interview data: {str(e)}")
        return jsonify({"error": f"Failed to store interview data: {str(e)}"}), 500

@app.route("/api/test-claude", methods=["GET"])
def test_claude_api():
    """Test endpoint for Claude API integration"""
    try:
        # Simple test analysis
        test_transcript = """
        Question: Please introduce yourself and your experience
        Answer: I am Zhang Ming, with 5 years of software development experience, mainly focusing on frontend development. I have worked in two tech companies and participated in the development of multiple large projects. I am skilled in React and Vue frameworks, with in-depth research in user experience and performance optimization. I love learning new technologies and often participate in tech sharing sessions and open source projects.
        
        Question: Why are you interested in this position?
        Answer: Your company's innovation capabilities and technical strength in the industry attracted me. I see that this position requires rich frontend development experience and team collaboration skills, which aligns perfectly with my skills and career development direction. I hope to continue growing in a more challenging environment and bring value to the team.
        """
        
        # Call Claude API for analysis
        result = analyze_with_claude(test_transcript, "Frontend Developer", "Test Candidate")
        
        return jsonify({
            "success": True,
            "message": "Claude API test successful",
            "result": result
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Claude API test failed: {str(e)}"
        })

@app.route("/intro")
def intro():
    return render_template("intro.html")

@app.route("/api/upload-resume", methods=["POST"])
def upload_resume():
    """Handle resume upload and text extraction"""
    try:
        resume_data = {}
        
        # Handle file upload
        if 'resume_file' in request.files:
            file = request.files['resume_file']
            if file.filename:
                # Save file temporarily
                temp_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(temp_path)
                
                # Extract text from file (implement based on file type)
                if file.filename.endswith('.pdf'):
                    # Use PyPDF2 or similar for PDF
                    import PyPDF2
                    with open(temp_path, 'rb') as pdf_file:
                        pdf_reader = PyPDF2.PdfReader(pdf_file)
                        text = ""
                        for page in pdf_reader.pages:
                            text += page.extract_text()
                        resume_data['text'] = text
                elif file.filename.endswith(('.doc', '.docx')):
                    # Use python-docx for Word documents
                    import docx
                    doc = docx.Document(temp_path)
                    text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
                    resume_data['text'] = text
                
                # Clean up temp file
                os.remove(temp_path)
        
        # Handle text input
        if 'resume_text' in request.form:
            resume_data['text'] = request.form['resume_text']
        
        if not resume_data:
            return jsonify({"error": "No resume data provided"}), 400
        
        return jsonify(resume_data)
        
    except Exception as e:
        print(f"Resume upload error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/generate-questions", methods=["POST"])
def generate_questions():
    """Generate interview questions based on resume and job position"""
    try:
        data = request.json
        candidate_name = data.get('candidate_name')
        job_position = data.get('job_position')
        interview_type = data.get('interview_type')
        resume_data = data.get('resume_data', {})
        
        # Construct prompt for AI
        prompt = f"""Generate 5 interview questions for a {interview_type} interview for the position of {job_position}.
        Candidate Name: {candidate_name}
        Resume Summary: {resume_data.get('text', '')}
        
        Please generate relevant questions that:
        1. Are specific to the candidate's experience and skills
        2. Match the job requirements
        3. Follow the interview type ({interview_type})
        4. Are professional and clear
        
        Return only the questions as a JSON array of strings."""
        
        # Use Claude API to generate questions
        try:
            response = chat_with_claude(prompt)
            # Parse the response to extract questions
            questions = json.loads(response)
            return jsonify({"questions": questions})
        except Exception as e:
            print(f"Claude API error: {e}")
            # Fallback to OpenAI if Claude fails
            response = chat_with_openai(prompt)
            questions = json.loads(response)
            return jsonify({"questions": questions})
            
    except Exception as e:
        print(f"Question generation error: {e}")
        return jsonify({"error": str(e)}), 500

# -----------------------------------------
# AI Resume Optimization Endpoint
# -----------------------------------------

# Shared helper to optimize resume text using available LLM

def optimize_text_with_ai(resume_text: str) -> str:
    """Return optimized resume text using OpenAI or Claude."""
    if not resume_text:
        raise ValueError("resume_text is empty")

    # Prefer OpenAI if key present
    if openai_api_key:
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # or latest available model
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an experienced career coach and ATS expert. "
                        "Improve the following resume content. Keep the tone professional and concise. "
                        "Return the optimized resume in markdown format."
                    ),
                },
                {"role": "user", "content": resume_text},
            ],
            max_tokens=1500,
        )
        return response.choices[0].message.content
    elif claude_api_key:
        return chat_with_claude(
            "You are an experienced career coach and ATS expert. Improve the following resume content. Keep the tone professional and concise. Return the optimized resume in markdown format.\n\n" + resume_text
        )
    else:
        raise EnvironmentError("No AI API key configured")

@app.route("/api/optimize-resume", methods=["POST"])
def optimize_resume():
    """Optimize resume text using configured LLM"""
    if not request.json or "resume_text" not in request.json:
        return jsonify({"error": "Please provide resume_text in JSON body"}), 400

    resume_text = request.json["resume_text"]

    # Decide which model to use based on available API keys.
    try:
        optimized_text = optimize_text_with_ai(resume_text)
        return jsonify({"optimized_resume": optimized_text})

    except Exception as e:
        print(f"Resume optimization error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Create command line argument parser
    parser = argparse.ArgumentParser(description='AIME Flask Web Application')
    parser.add_argument('--port', type=int, default=5010, help='Port number to run the server on')
    
    # Parse command line arguments
    args = parser.parse_args()
    
    # Use specified port to run the application
    app.run(debug=True, port=args.port)
