"""
Jana's Bot - Personal RAG Chatbot
"""

import os
import streamlit as st
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader
import tempfile
import shutil
import pickle
from pathlib import Path

# API Key Configuration
# Will be loaded from Streamlit secrets (cloud) or environment variable (local)
API_KEY = None
PERSIST_DIRECTORY = "./faiss_db"
RESUME_PATH = "./resume.pdf"
FAISS_INDEX_PATH = "./faiss_db/index.faiss"
FAISS_PKL_PATH = "./faiss_db/index.pkl"

class ChatBot:
    def __init__(self):
        # Set API key in environment first (required)
        if API_KEY is None:
            raise ValueError("API_KEY not set. Please set it in main() first.")
        os.environ["OPENAI_API_KEY"] = API_KEY
        
        # Initialize embeddings - uses OPENAI_API_KEY from environment
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            # Initialize embeddings - handle version compatibility issues
            # Remove any proxy-related environment variables that might cause issues
            env_backup = {}
            for key in list(os.environ.keys()):
                if 'proxy' in key.lower() or 'PROXY' in key:
                    env_backup[key] = os.environ.pop(key)
            
            # Initialize embeddings - use environment variable only to avoid ValidationError
            # Ensure API key is set in environment
            os.environ["OPENAI_API_KEY"] = API_KEY
            
            # Remove any problematic environment variables that might cause validation errors
            # Some versions of langchain-openai have issues with certain env vars
            
            # Initialize with minimal configuration - only use environment variable
            # This avoids passing parameters that might trigger pydantic validation errors
            # Try delayed initialization to avoid pydantic v1 issues
            import sys
            import importlib
            
            # Clear any cached imports that might have old versions
            if 'langchain_openai' in sys.modules:
                importlib.reload(sys.modules['langchain_openai'])
            
            # Initialize embeddings - always use model parameter to avoid ValidationError
            # The model parameter helps bypass pydantic v1 validation issues
            # Ensure API key is in environment
            os.environ["OPENAI_API_KEY"] = API_KEY
            
            # Always use model parameter - this is more reliable with pydantic v1
            try:
                self.embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
            except Exception as e:
                # If model parameter fails, try without it
                try:
                    self.embeddings = OpenAIEmbeddings()
                except Exception:
                    # Store for delayed initialization
                    self._api_key = API_KEY
                    self.embeddings = None
            finally:
                # Restore environment variables
                os.environ.update(env_backup)
                # Always ensure API key is set
                os.environ["OPENAI_API_KEY"] = API_KEY
        
        # Initialize LLM - use environment variable
        try:
            self.llm = ChatOpenAI(
                model="gpt-3.5-turbo",
                temperature=0.7
            )
        except Exception:
            # Fallback
            self.llm = ChatOpenAI(temperature=0.7)
        
        self.vectorstore = None
        self.qa_chain = None
        
    def initialize_vectorstore(self):
        """Initialize or load existing vector store"""
        # Ensure directory exists
        try:
            os.makedirs(PERSIST_DIRECTORY, exist_ok=True)
            
            # Check if FAISS index already exists
            if os.path.exists(FAISS_INDEX_PATH) and os.path.exists(FAISS_PKL_PATH):
                try:
                    self.vectorstore = FAISS.load_local(
                        PERSIST_DIRECTORY,
                        self.embeddings,
                        allow_dangerous_deserialization=True
                    )
                    return True
                except Exception as e:
                    # If loading fails, recreate
                    if os.path.exists(PERSIST_DIRECTORY):
                        shutil.rmtree(PERSIST_DIRECTORY)
                    os.makedirs(PERSIST_DIRECTORY, exist_ok=True)
                    self.vectorstore = None
                    return False
            else:
                # No existing index
                self.vectorstore = None
                if os.path.exists(RESUME_PATH):
                    if self.load_documents([RESUME_PATH]):
                        return True
                return False
        except Exception as e:
            # Clean up and try again
            try:
                if os.path.exists(PERSIST_DIRECTORY):
                    shutil.rmtree(PERSIST_DIRECTORY)
                os.makedirs(PERSIST_DIRECTORY, exist_ok=True)
                self.vectorstore = None
                return False
            except:
                return False
    
    def load_documents(self, file_paths):
        """Load and process documents"""
        # FAISS doesn't need pre-initialization - we'll create it with documents
        
        documents = []
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        
        for file_path in file_paths:
            file_ext = Path(file_path).suffix.lower()
            
            # Check if file exists
            if not os.path.exists(file_path):
                st.error(f"File not found: {file_path}")
                return False
            
            try:
                if file_ext == '.pdf':
                    loader = PyPDFLoader(file_path)
                    docs = loader.load()
                    st.info(f"Loaded {len(docs)} pages from PDF")
                elif file_ext in ['.txt', '.md']:
                    loader = TextLoader(file_path)
                    docs = loader.load()
                    st.info(f"Loaded text file")
                else:
                    st.error(f"Unsupported file type: {file_ext}")
                    return False
                
                if not docs or len(docs) == 0:
                    st.error("Document is empty - no content found")
                    return False
                
                # Split documents
                split_docs = text_splitter.split_documents(docs)
                documents.extend(split_docs)
                st.info(f"Created {len(split_docs)} document chunks")
                
            except Exception as e:
                error_msg = str(e)
                st.error(f"Error loading file: {error_msg}")
                import traceback
                st.error(f"Details: {traceback.format_exc()}")
                return False
        
        if documents and len(documents) > 0:
            try:
                # Ensure directory exists
                os.makedirs(PERSIST_DIRECTORY, exist_ok=True)
                
                # Create FAISS vectorstore from documents
                st.info("Creating embeddings and vector database...")
                self.vectorstore = FAISS.from_documents(documents, self.embeddings)
                
                # Save FAISS index
                st.info("Saving vector database...")
                self.vectorstore.save_local(PERSIST_DIRECTORY)
                
                st.success(f"Successfully created vector database with {len(documents)} chunks")
                return True
                    
            except Exception as e:
                error_msg = str(e)
                st.error(f"Error creating vectorstore: {error_msg}")
                import traceback
                with st.expander("Error Details"):
                    st.code(traceback.format_exc())
                return False
        else:
            st.error("No documents to add - processing failed")
            return False
    
    def setup_qa_chain(self):
        """Setup the question-answering chain"""
        if self.vectorstore is None:
            # Try to load existing FAISS index
            if os.path.exists(FAISS_INDEX_PATH) and os.path.exists(FAISS_PKL_PATH):
                try:
                    self.vectorstore = FAISS.load_local(
                        PERSIST_DIRECTORY,
                        self.embeddings,
                        allow_dangerous_deserialization=True
                    )
                except:
                    return False
            else:
                return False
        
        retriever = self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 4}
        )
        
        # Custom prompt to encourage natural language generation
        prompt_template = """You are Jana's friendly chatbot assistant. Be warm, conversational, and helpful.

If the question is a greeting (like "hi", "hello", "hey"), respond warmly and introduce yourself. For example:
- "Hi! I'm Jana's Bot. I'm here to help answer questions about Jana's background, experience, skills, and qualifications. What would you like to know?"
- "Hello! Nice to meet you! I can tell you about Jana's professional experience, education, and skills. Feel free to ask me anything!"

For other questions, use the following pieces of context from Jana's resume to answer. Provide a clear, natural, and conversational answer in your own words. Don't just copy text verbatim - synthesize the information and explain it naturally.

If you don't know the answer based on the context, say so politely.

Context: {context}

Question: {question}

Answer in a friendly, natural, conversational way:"""
        
        PROMPT = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            chain_type_kwargs={"prompt": PROMPT},
            return_source_documents=False
        )
        return True
    
    def get_response(self, question):
        """Get response from chatbot"""
        if self.qa_chain is None:
            return None
        
        try:
            # Make sure we have a proper query
            if not question or len(question.strip()) == 0:
                return "Please ask a question about Jana."
            
            result = self.qa_chain.invoke({"query": question})
            
            # Check if we got a valid result
            if result and "result" in result:
                return result["result"]
            else:
                return "I couldn't generate a response. Please try rephrasing your question."
        except Exception as e:
            # Return error message for debugging
            error_msg = str(e)
            if "api" in error_msg.lower() or "openai" in error_msg.lower():
                return f"API Error: {error_msg}. Please check your API key."
            return f"Error processing question: {error_msg}"

def main():
    st.set_page_config(
        page_title="Jana's Bot - Admin",
        page_icon="⚙️",
        layout="centered"
    )
    
    # Get API key from Streamlit secrets (cloud) or environment variable (local)
    global API_KEY
    
    # Try Streamlit secrets first (for cloud deployment)
    try:
        if hasattr(st, 'secrets') and 'OPENAI_API_KEY' in st.secrets:
            API_KEY = st.secrets["OPENAI_API_KEY"]
            os.environ["OPENAI_API_KEY"] = API_KEY
        elif os.getenv("OPENAI_API_KEY"):
            # Fallback to environment variable (for local development)
            API_KEY = os.getenv("OPENAI_API_KEY")
        else:
            st.error("❌ **API Key Missing!** Please set `OPENAI_API_KEY` in Streamlit Secrets (cloud) or environment variable (local).")
            st.stop()
    except Exception as e:
        st.error(f"❌ **Error loading API key:** {str(e)}")
        st.stop()
    
    # Light pink theme
    st.markdown("""
    <style>
        /* Hide deploy button only */
        .stDeployButton {
            display: none;
        }
        
        /* Bottom header/footer styling - Make visible with pink theme */
        footer {
            visibility: visible !important;
            background-color: rgba(255, 182, 193, 0.1) !important;
        }
        
        footer * {
            color: #ffb6c1 !important;
        }
        
        [data-testid="stFooter"] {
            background-color: rgba(255, 182, 193, 0.1) !important;
        }
        
        [data-testid="stFooter"] * {
            color: #ffb6c1 !important;
        }
        
        /* Any bottom elements */
        .footer h1, .footer h2, .footer h3,
        .footer h4, .footer h5, .footer h6,
        .footer *, footer h1, footer h2, footer h3,
        footer h4, footer h5, footer h6,
        footer p, footer span, footer div {
            color: #ffb6c1 !important;
        }
        
        /* Bottom section headers */
        .stApp > footer h1, .stApp > footer h2, .stApp > footer h3 {
            color: #ffb6c1 !important;
        }
        
        /* Light pink theme */
        .stApp {
            background: linear-gradient(135deg, #ffeef7 0%, #fff5f9 50%, #ffeef7 100%);
        }
        
        .main .block-container {
            max-width: 800px;
            padding: 2rem 1rem;
            background-color: rgba(255, 255, 255, 0.9);
            border-radius: 15px;
            box-shadow: 0 4px 20px rgba(255, 182, 193, 0.2);
        }
        
        /* All Headers - Light Pink - Universal */
        h1, h2, h3, h4, h5, h6 {
            color: #ffb6c1 !important;
            font-weight: 600;
        }
        
        /* Streamlit app header area */
        [data-testid="stHeader"] {
            background-color: rgba(255, 182, 193, 0.1) !important;
        }
        
        [data-testid="stHeader"] * {
            color: #ffb6c1 !important;
        }
        
        /* Any header elements anywhere */
        header h1, header h2, header h3, header h4, header h5, header h6,
        .header h1, .header h2, .header h3, .header h4, .header h5, .header h6,
        header *, .header * {
            color: #ffb6c1 !important;
        }
        
        /* Streamlit title elements */
        .stTitle h1, .stTitle h2, .stTitle h3,
        .stTitle h4, .stTitle h5, .stTitle h6,
        .stTitle * {
            color: #ffb6c1 !important;
        }
        
        /* All markdown headers */
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
        .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
            color: #ffb6c1 !important;
        }
        
        /* Streamlit element containers with headers */
        .element-container h1, .element-container h2, .element-container h3,
        .element-container h4, .element-container h5, .element-container h6 {
            color: #ffb6c1 !important;
        }
        
        /* Main content area headers */
        .main h1, .main h2, .main h3,
        .main h4, .main h5, .main h6 {
            color: #ffb6c1 !important;
        }
        
        /* Block container headers */
        .block-container h1, .block-container h2, .block-container h3,
        .block-container h4, .block-container h5, .block-container h6 {
            color: #ffb6c1 !important;
        }
        
        /* Force all heading tags globally */
        * h1, * h2, * h3, * h4, * h5, * h6 {
            color: #ffb6c1 !important;
        }
        
        /* All text - Darker Pink */
        p, div, span, label, .stMarkdown {
            color: #c2185b !important;
        }
        
        /* Chat messages */
        .stChatMessage {
            background-color: rgba(255, 240, 245, 0.8);
            border-radius: 10px;
            padding: 1rem;
            margin: 0.5rem 0;
        }
        
        .stChatMessage p, .stChatMessage div {
            color: #c2185b !important;
        }
        
        /* Buttons */
        .stButton > button {
            background-color: #ffb6c1;
            color: #c2185b !important;
            border: none;
            border-radius: 20px;
            padding: 0.5rem 2rem;
            font-weight: 500;
        }
        
        .stButton > button:hover {
            background-color: #ff91a4;
            color: #c2185b !important;
        }
        
        /* Primary buttons */
        .stButton > button[kind="primary"] {
            background-color: #ffb6c1;
            color: #c2185b !important;
        }
        
        .stButton > button[kind="primary"]:hover {
            background-color: #ff91a4;
            color: #c2185b !important;
        }
        
        /* Input */
        .stTextInput > div > div > input {
            border-color: #ffb6c1;
            border-radius: 10px;
            color: #c2185b !important;
        }
        
        .stTextInput label {
            color: #c2185b !important;
        }
        
        /* File uploader */
        .stFileUploader {
            border: 2px dashed #ffb6c1;
            border-radius: 10px;
            background-color: rgba(255, 240, 245, 0.5);
        }
        
        .stFileUploader label {
            color: #c2185b !important;
        }
        
        /* Chat input */
        .stChatInputContainer {
            background-color: rgba(255, 240, 245, 0.9);
            border-radius: 15px;
        }
        
        .stChatInputContainer input {
            color: #c2185b !important;
        }
        
        /* Success messages */
        .stSuccess {
            background-color: #ffb6c1;
            color: #c2185b !important;
        }
        
        /* Info boxes */
        .stInfo {
            background-color: rgba(255, 182, 193, 0.2);
            border-left: 4px solid #ffb6c1;
            color: #c2185b !important;
        }
        
        /* Warning boxes */
        .stWarning {
            background-color: rgba(255, 182, 193, 0.3);
            border-left: 4px solid #ff91a4;
            color: #c2185b !important;
        }
        
        /* Error boxes */
        .stError {
            background-color: rgba(255, 182, 193, 0.4);
            border-left: 4px solid #e91e63;
            color: #c2185b !important;
        }
        
        /* All markdown text */
        .stMarkdown p, .stMarkdown div, .stMarkdown {
            color: #c2185b !important;
        }
        
        /* Chat bubbles */
        [data-testid="stChatMessage"] p, [data-testid="stChatMessage"] div {
            color: #c2185b !important;
        }
        
        /* All Streamlit text elements */
        .element-container p, .element-container div, .element-container span {
            color: #c2185b !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize chatbot
    if "bot" not in st.session_state:
        st.session_state.bot = ChatBot()
        if st.session_state.bot.initialize_vectorstore():
            if st.session_state.bot.setup_qa_chain():
                st.session_state.resume_loaded = True
            else:
                st.session_state.resume_loaded = False
        else:
            st.session_state.resume_loaded = False
    
    # Fix: If resume_loaded is True but QA chain isn't ready, fix it
    if st.session_state.resume_loaded:
        if not st.session_state.bot or not st.session_state.bot.qa_chain:
            # Try to reload from existing database
            if os.path.exists(PERSIST_DIRECTORY) and os.listdir(PERSIST_DIRECTORY):
                try:
                    st.session_state.bot = ChatBot()
                    if st.session_state.bot.initialize_vectorstore():
                        if st.session_state.bot.setup_qa_chain():
                            st.session_state.resume_loaded = True
                        else:
                            st.session_state.resume_loaded = False
                except:
                    st.session_state.resume_loaded = False
            else:
                st.session_state.resume_loaded = False
    
    # Title
    st.title("Jana's Bot")
    st.write("Ask questions about Jana based on her resume")
    
    # Upload Section
    st.header("Upload Resume")
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=["pdf"],
        help="Upload Jana's resume in PDF format"
    )
    
    if uploaded_file is not None:
        # Show file info
        st.markdown("---")
        st.markdown(f"### 📄 Selected File")
        st.success(f"**{uploaded_file.name}** ({uploaded_file.size / 1024:.1f} KB)")
        st.write("")  # Spacing
        
        # Load button - make it VERY visible with instructions
        st.markdown("**⚠️ IMPORTANT: Click the button below to process your resume**")
        st.write("")
        
        # Big, visible button
        load_button = st.button(
            "📄 LOAD RESUME NOW", 
            type="primary", 
            use_container_width=True,
            help="Click this button to process and load your resume",
            key="load_resume_button"
        )
        
        if not load_button:
            st.info("👆 Click the 'LOAD RESUME NOW' button above to process your file")
        
        if load_button:
            # Progress container
            progress_container = st.container()
            with progress_container:
                st.markdown("### Processing Your Resume...")
                
                temp_dir = None
                try:
                    # Step 1: Save file
                    st.markdown("**Step 1:** Saving uploaded file...")
                    temp_dir = tempfile.mkdtemp()
                    file_path = os.path.join(temp_dir, uploaded_file.name)
                    
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    if not os.path.exists(file_path):
                        st.error("❌ Failed to save file")
                        return
                    
                    file_size = os.path.getsize(file_path)
                    st.success(f"✅ File saved ({file_size:,} bytes)")
                    st.write("")
                    
                    # Step 2: Clear old database
                    st.markdown("**Step 2:** Clearing old database...")
                    if os.path.exists(PERSIST_DIRECTORY):
                        try:
                            shutil.rmtree(PERSIST_DIRECTORY)
                            st.success("✅ Database cleared")
                        except Exception as e:
                            st.warning(f"⚠️ Could not clear database: {str(e)}")
                            # Continue anyway
                    else:
                        st.info("✅ No existing database to clear")
                    # Ensure directory exists with proper permissions
                    os.makedirs(PERSIST_DIRECTORY, exist_ok=True)
                    # Fix permissions
                    import stat
                    os.chmod(PERSIST_DIRECTORY, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
                    st.success("✅ Database directory ready")
                    st.write("")
                    
                    # Step 3: Initialize bot
                    st.markdown("**Step 3:** Initializing chatbot...")
                    st.session_state.bot = ChatBot()
                    st.success("✅ Chatbot initialized")
                    st.write("")
                    
                    # Step 4: Load documents
                    st.markdown("**Step 4:** Processing PDF and creating embeddings...")
                    st.warning("This step takes 30-60 seconds. Please wait...")
                    
                    if st.session_state.bot.load_documents([file_path]):
                        st.success("✅ Documents processed")
                        st.write("")
                        
                        # Step 5: Setup QA chain
                        st.markdown("**Step 5:** Setting up question-answering system...")
                        if st.session_state.bot.setup_qa_chain():
                            st.success("✅ QA system ready")
                            st.write("")
                            
                            # Save resume
                            if not os.path.exists(RESUME_PATH):
                                shutil.copy2(file_path, RESUME_PATH)
                            
                            st.session_state.resume_loaded = True
                            st.balloons()
                            st.success("🎉 **Resume loaded successfully!** You can now ask questions below.")
                        else:
                            st.error("❌ Failed to setup QA chain")
                            st.info("Try clicking 'LOAD RESUME NOW' again")
                    else:
                        st.error("❌ Failed to process document")
                        st.info("Check error messages above and try again")
                    
                    # Cleanup
                    if temp_dir and os.path.exists(temp_dir):
                        shutil.rmtree(temp_dir)
                    
                    # Small delay before rerun
                    import time
                    time.sleep(1)
                    st.rerun()
                    
                except Exception as e:
                    error_msg = str(e)
                    st.error(f"❌ **Error:** {error_msg}")
                    import traceback
                    with st.expander("📋 Click to see full error details"):
                        st.code(traceback.format_exc())
                    
                    st.info("💡 **Try this:** Refresh the page and upload your resume again.")
                    
                    if temp_dir and os.path.exists(temp_dir):
                        shutil.rmtree(temp_dir)
    
    # Status with debug info
    if st.session_state.resume_loaded:
        # Verify everything is actually set up
        if st.session_state.bot and st.session_state.bot.qa_chain:
            st.success("✅ Resume is loaded and ready!")
        else:
            st.warning("⚠️ Resume marked as loaded but QA chain not ready.")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔧 Auto-Fix", type="primary"):
                    # Try to reload from existing database
                    try:
                        st.session_state.bot = ChatBot()
                        if st.session_state.bot.initialize_vectorstore():
                            if st.session_state.bot.setup_qa_chain():
                                st.success("✅ Fixed! Resume is ready.")
                            else:
                                st.error("❌ Could not setup QA chain. Please reload resume.")
                        else:
                            st.error("❌ Could not load vectorstore. Please reload resume.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
            with col2:
                if st.button("📄 Upload New Resume"):
                    st.session_state.resume_loaded = False
                    st.session_state.bot = None
                    st.rerun()
    else:
        st.warning("No resume loaded. Upload a PDF above and click 'Load Resume'.")
    
    st.divider()
    
    # Chat interface
    st.header("Chat")
    
    # Initialize messages
    if "messages" not in st.session_state:
        st.session_state.messages = []
        if not st.session_state.resume_loaded:
            st.session_state.messages.append({
                "role": "assistant",
                "content": "Hi there! 👋 I'm Jana's Bot! Please upload a resume PDF above to get started. Once loaded, I'll be happy to answer questions about Jana's background, experience, skills, education, and qualifications. Feel free to ask me anything!"
            })
        else:
            st.session_state.messages.append({
                "role": "assistant",
                "content": "Hi there! 👋 I'm Jana's Bot, and I'm ready to help! I can answer questions about Jana based on her resume. What would you like to know? Feel free to ask me anything - I'm here to chat!"
            })
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about Jana..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Show user message
        with st.chat_message("user"):
            st.write(prompt)
        
        # Get bot response
        with st.chat_message("assistant"):
            if not st.session_state.resume_loaded:
                response = "Please upload a resume PDF first using the upload section above, then click 'Load Resume'."
            else:
                # Check if bot and QA chain are ready
                if st.session_state.bot is None:
                    response = "Bot not initialized. Please reload the page."
                elif st.session_state.bot.qa_chain is None:
                    response = "QA chain not set up. Please reload your resume."
                else:
                    with st.spinner("Thinking..."):
                        try:
                            response = st.session_state.bot.get_response(prompt)
                            if response is None or response == "":
                                response = "I'm sorry, I couldn't generate a response. Please try rephrasing your question."
                        except Exception as e:
                            response = f"Error: {str(e)}. Please try again or reload the resume."
            
            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
