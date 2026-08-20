from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_anthropic import ChatAnthropic
import time
import os
import json
import uuid
import os
from datetime import datetime

# Set environment variables to avoid tokenizers warnings
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Read Claude API key from environment variable
claude_api_key = os.getenv("CLAUDE_API_KEY")
if not claude_api_key:
    raise EnvironmentError("CLAUDE_API_KEY environment variable is not set. Please configure it in your environment or .env file.")

# Define text cleaning function
def clean_text(text):
    """Simple text cleaning function"""
    if not text:
        return ""
    # Remove excess whitespace
    text = ' '.join(text.split())
    return text

class AIme:
    """AIme - MBTI-based study abroad essay RAG system"""
    
    def __init__(self, data_dir="data", model_name="sentence-transformers/all-mpnet-base-v2", session_id=None):
        try:
            # Ensure data directory exists
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)
                print(f"Created data directory: {data_dir}")
                # Create a sample file for system loading
                with open(f"{data_dir}/example.txt", "w", encoding="utf-8") as f:
                    f.write("MBTI (Myers-Briggs Type Indicator) is a personality type assessment tool that divides human personality into 16 types.\n")
                    f.write("MBTI is based on four dimensions: Extraversion (E) vs. Introversion (I), Sensing (S) vs. Intuition (N), Thinking (T) vs. Feeling (F), and Judging (J) vs. Perceiving (P).\n")
                    f.write("In study abroad essays, showcasing your MBTI type can help admissions officers gain a more comprehensive understanding of the applicant's personality traits and thinking style.\n")
            
            # 1. Load documents - only process text files
            from langchain_community.document_loaders import TextLoader
            import glob
            
            # Replace existing loader code
            self.documents = []
            text_files = glob.glob(f"{data_dir}/**/*.txt", recursive=True)
            
            # Check if text files are found
            if not text_files:
                print(f"Warning: No text files found in {data_dir} directory")
                # Create a sample file for system loading
                example_file = f"{data_dir}/example.txt"
                with open(example_file, "w", encoding="utf-8") as f:
                    f.write("MBTI (Myers-Briggs Type Indicator) is a personality type assessment tool that divides human personality into 16 types.\n")
                    f.write("MBTI is based on four dimensions: Extraversion (E) vs. Introversion (I), Sensing (S) vs. Intuition (N), Thinking (T) vs. Feeling (F), and Judging (J) vs. Perceiving (P).\n")
                    f.write("In study abroad essays, showcasing your MBTI type can help admissions officers gain a more comprehensive understanding of the applicant's personality traits and thinking style.\n")
                text_files = [example_file]
                print(f"Created example file: {example_file}")
            
            for text_file in text_files:
                try:
                    loader = TextLoader(text_file, encoding="utf-8") # Added encoding for safety
                    self.documents.extend(loader.load())
                    print(f"Loaded file: {text_file}")
                except Exception as e:
                    print(f"Error loading file {text_file}: {str(e)}")
            
            # Ensure at least one document
            if not self.documents:
                raise ValueError("No documents successfully loaded, please check file format or permissions")
            
            # 2. Document cleaning
            for doc in self.documents:
                doc.page_content = clean_text(doc.page_content)
            
            # 3. Split documents
            self.text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            self.texts = self.text_splitter.split_documents(self.documents)
            
            # 4. Create embeddings and vector store
            self.embeddings = HuggingFaceEmbeddings(model_name=model_name)
            self.vectorstore = FAISS.from_documents(self.texts, self.embeddings)
            
            # 5. Initialize Claude
            self.llm = ChatAnthropic(
                temperature=0.7,  # Increase creativity
                model_name="claude-3-opus-20240229",
                anthropic_api_key=claude_api_key
            )
            
            # 6. Create retrieval chain
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=self.vectorstore.as_retriever(
                    search_type="mmr",  # Use maximum marginal relevance search
                    search_kwargs={"k": 5}  # Increase number of returned documents
                )
            )
            
            # MBTI type list
            self.mbti_types = [
                "ISTJ", "ISFJ", "INFJ", "INTJ",
                "ISTP", "ISFP", "INFP", "INTP",
                "ESTP", "ESFP", "ENFP", "ENTP",
                "ESTJ", "ESFJ", "ENFJ", "ENTJ"
            ]
            
            # Add conversation history storage
            self.conversation_history = []
            
            # Session management
            self.sessions_dir = "sessions"
            if not os.path.exists(self.sessions_dir):
                os.makedirs(self.sessions_dir)
                
            # Create or load session
            if session_id:
                self.session_id = session_id
                self.load_session(session_id)
            else:
                self.session_id = str(uuid.uuid4())
                self.conversation_history = []
                self.session_metadata = {
                    "created_at": datetime.now().isoformat(),
                    "mbti_type": None,
                    "last_accessed": datetime.now().isoformat()
                }
                self.save_session()
            
            print("AIme initialization completed! I'm your MBTI study abroad essay assistant")
        except Exception as e:
            raise RuntimeError(f"AIme initialization failed: {str(e)}")
    
    def query(self, current_question, mbti_type=None, chat_history=None):
        """Query AIme system (supports context and RAG)"""
        # If no history provided, use internally stored history
        if chat_history is None:
            chat_history = self.conversation_history
            
        start_time = time.time()
        try:
            # Add MBTI type to question
            if mbti_type and mbti_type.upper() in self.mbti_types:
                enhanced_question = f"For people with MBTI type {mbti_type.upper()}, {current_question}"
            else:
                enhanced_question = current_question

            # Retrieve relevant documents (RAG)
            retrieved_docs = self.vectorstore.similarity_search(enhanced_question, k=3)
            context = "\n".join([doc.page_content for doc in retrieved_docs])

            # Construct conversation history
            messages = [
                {"role": "system", "content": "You are AIme, an AI assistant that knows about MBTI and studying abroad."},
                {"role": "system", "content": f"Here is the relevant information about the user's question:\n{context}"}
            ]

            # Insert historical dialogue
            messages.extend(chat_history)

            # Add current question
            messages.append({"role": "user", "content": enhanced_question})

            # Add current question to history
            self.conversation_history.append({"role": "user", "content": enhanced_question})
            
            # Call Claude LLM
            response = self.llm.invoke(messages)
            
            # Add answer to history
            self.conversation_history.append({"role": "assistant", "content": response.content})
            
            # Save session before method ends
            if mbti_type:
                self.session_metadata["mbti_type"] = mbti_type
            self.session_metadata["last_accessed"] = datetime.now().isoformat()
            self.save_session()
            
            elapsed = time.time() - start_time
            print(f"Query processing time: {elapsed:.2f} seconds")
            return response

        except Exception as e:
            return f"Query processing error: {str(e)}"
    
    def generate_essay(self, mbti_type, topic, word_count=500):
        """Generate a study abroad essay based on MBTI type"""
        if mbti_type.upper() not in self.mbti_types:
            return f"Error: {mbti_type} is not a valid MBTI type. Please provide a valid MBTI type (e.g., ENFJ, ISTP, etc.)."
        
        prompt = f"""
        Please write a study abroad essay for a person with MBTI type {mbti_type.upper()}.
        The essay should highlight the person's strengths and advantages based on their MBTI type.
        The essay should be genuine and personalized, avoiding template use or overly elaborate language.
        The essay should be about {topic}, and it should be approximately {word_count} words long.
        """
        
        return self.query(prompt, mbti_type)
    
    def analyze_mbti(self, mbti_type):
        """Analyze the characteristics and advantages of a specific MBTI type in studying abroad applications"""
        if mbti_type.upper() not in self.mbti_types:
            return f"Error: {mbti_type} is not a valid MBTI type. Please provide a valid MBTI type (e.g., ENFJ, ISTP, etc.)."
        
        prompt = f"""
        Please analyze the characteristics and advantages of people with MBTI type {mbti_type.upper()} in terms of personality, learning, work, and social interactions.
        How do these characteristics become advantages in studying abroad applications?
        When writing a study abroad essay, what should people with {mbti_type.upper()} type do to showcase their strengths and overcome potential weaknesses?
        Please provide specific essay writing suggestions and examples.
        """
        
        return self.query(prompt, mbti_type)
    
    def save_session(self):
        """Save current session to file"""
        session_data = {
            "session_id": self.session_id,
            "conversation_history": self.conversation_history,
            "metadata": self.session_metadata
        }
        
        with open(f"{self.sessions_dir}/{self.session_id}.json", "w", encoding="utf-8") as f:
            json.dump(session_data, f, ensure_ascii=False, indent=2)
    
    def load_session(self, session_id):
        """Load session from file"""
        try:
            with open(f"{self.sessions_dir}/{session_id}.json", "r", encoding="utf-8") as f:
                session_data = json.load(f)
                
            self.conversation_history = session_data.get("conversation_history", [])
            self.session_metadata = session_data.get("metadata", {})
            self.session_metadata["last_accessed"] = datetime.now().isoformat()
            
        except FileNotFoundError:
            print(f"Session {session_id} does not exist, creating new session")
            self.session_id = str(uuid.uuid4())
            self.conversation_history = []
            self.session_metadata = {
                "created_at": datetime.now().isoformat(),
                "mbti_type": None,
                "last_accessed": datetime.now().isoformat()
            }
    
    def list_sessions(self):
        """List all available sessions"""
        sessions = []
        for filename in os.listdir(self.sessions_dir):
            if filename.endswith(".json"):
                try:
                    with open(f"{self.sessions_dir}/{filename}", "r", encoding="utf-8") as f:
                        session_data = json.load(f)
                        sessions.append({
                            "session_id": session_data.get("session_id"),
                            "created_at": session_data.get("metadata", {}).get("created_at"),
                            "last_accessed": session_data.get("metadata", {}).get("last_accessed"),
                            "mbti_type": session_data.get("metadata", {}).get("mbti_type"),
                            "message_count": len(session_data.get("conversation_history", []))
                        })
                except Exception as e:
                    print(f"Error reading session file {filename}: {str(e)}")
        
        return sessions

# Usage example
if __name__ == "__main__":
    try:
        print("Initializing AIme system...")
        
        # Check if there is an existing session
        sessions_dir = "sessions"
        if os.path.exists(sessions_dir) and os.listdir(sessions_dir):
            print("\nFound existing sessions:")
            session_files = [f for f in os.listdir(sessions_dir) if f.endswith(".json")]
            
            for i, session_file in enumerate(session_files):
                try:
                    with open(f"{sessions_dir}/{session_file}", "r", encoding="utf-8") as f:
                        session_data = json.load(f)
                        metadata = session_data.get("metadata", {})
                        print(f"{i+1}. Session ID: {session_data.get('session_id')} - Created at: {metadata.get('created_at')} - MBTI type: {metadata.get('mbti_type') or 'Not set'}")
                except Exception:
                    print(f"{i+1}. {session_file} (Details cannot be read)")
            
            print(f"{len(session_files)+1}. Create new session")
            
            choice = input("\nPlease choose session (Enter number): ")
            try:
                choice_num = int(choice)
                if 1 <= choice_num <= len(session_files):
                    session_id = session_files[choice_num-1].replace(".json", "")
                    aime = AIme(session_id=session_id)
                    print(f"Loaded session: {session_id}")
                else:
                    aime = AIme()
                    print("Created new session")
            except ValueError:
                aime = AIme()
                print("Invalid input, created new session")
        else:
            aime = AIme()
            print("No existing sessions found, created new session")
        
        while True:
            print("\n===== AIme - Your MBTI Study Abroad Essay Assistant =====")
            print("1. Ask questions about MBTI and study abroad essays")
            print("2. Analyze the characteristics and advantages of a specific MBTI type")
            print("3. Generate a study abroad essay based on MBTI type")
            print("4. View conversation history")
            print("5. Clear conversation history")
            print("6. Exit")
            
            choice = input("\nPlease choose function (1-6): ")
            
            if choice == "1":
                question = input("Please enter your question: ")
                print("\nThinking...")
                result = aime.query(question)
                print(f"\nAnswer: {result.content}")
            
            elif choice == "2":
                mbti_type = input("Please enter MBTI type (e.g., ENFJ): ").upper()
                print("\nAnalyzing...")
                result = aime.analyze_mbti(mbti_type)
                print(f"\nAnalysis result: {result}") # Assuming result from analyze_mbti is already a string
            
            elif choice == "3":
                mbti_type = input("Please enter MBTI type (e.g., ENFJ): ").upper()
                topic = input("Please enter essay topic: ")
                word_count = input("Please enter expected word count (default 500): ")
                if not word_count:
                    word_count = 500
                else:
                    word_count = int(word_count)
                
                print("\nGenerating essay...")
                result = aime.generate_essay(mbti_type, topic, word_count)
                # Assuming result from generate_essay is an AIMessage object or similar, access content if needed
                # If result is already a string, this is fine. If it's an object, use result.content or similar.
                print(f"\nGenerated essay: \n{result}") 
            
            elif choice == "4":
                # Display conversation history
                if not aime.conversation_history:
                    print("\nNo conversation history")
                else:
                    print("\n===== Conversation History =====")
                    for i, msg in enumerate(aime.conversation_history):
                        role = "User" if msg["role"] == "user" else "AIme"
                        print(f"{i+1}. {role}: {msg['content'][:50]}...") # Displaying first 50 chars
            
            elif choice == "5":
                # Clear conversation history
                aime.conversation_history = []
                # Also update the session file to reflect the cleared history
                aime.save_session() 
                print("\nConversation history cleared and session saved.")
            
            elif choice == "6":
                print("Thank you for using AIme! Goodbye!")
                break
            
            else:
                print("Invalid choice, please enter again.")
                
    except Exception as e:
        print(f"Error: {str(e)}")