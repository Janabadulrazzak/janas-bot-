"""
Jana's Bot - User-Facing Chat Interface
This is the public-facing page - users can only chat, no document upload
"""

import os
import streamlit as st
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# API Key Configuration
# Will be loaded from Streamlit secrets (cloud) or environment variable (local)
API_KEY = None
PERSIST_DIRECTORY = "./faiss_db"
FAISS_INDEX_PATH = "./faiss_db/index.faiss"
FAISS_PKL_PATH = "./faiss_db/index.pkl"

class UserChatBot:
    def __init__(self):
        if API_KEY is None:
            raise ValueError("API_KEY not set. Please set it in main() first.")
        os.environ["OPENAI_API_KEY"] = API_KEY
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
            
            # Initialize embeddings - handle ValidationError from pydantic v1
            # The issue is langchain-openai uses pydantic v1 internally
            try:
                # Try to import and catch ValidationError specifically
                from pydantic.v1.error_wrappers import ValidationError as PydanticV1ValidationError
            except ImportError:
                PydanticV1ValidationError = Exception
            
            try:
                # Try with no parameters first - this should work if API key is in env
                self.embeddings = OpenAIEmbeddings()
            except PydanticV1ValidationError as ve:
                # If it's a pydantic v1 validation error, try to bypass it
                # by setting the API key in environment and using a different approach
                try:
                    # Try using the class with explicit model name
                    from langchain_openai.embeddings import OpenAIEmbeddings as LCEmbeddings
                    self.embeddings = LCEmbeddings(model="text-embedding-ada-002")
                except Exception:
                    # If that fails, we'll need to delay initialization
                    # Store the API key for later initialization
                    self._api_key = API_KEY
                    self.embeddings = None
                    # Don't show warning in __init__ - handle it when needed
            except Exception as e:
                # For any other error, try one more time with model parameter
                try:
                    self.embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
                except Exception:
                    self._api_key = API_KEY
                    self.embeddings = None
            finally:
                # Restore environment variables
                os.environ.update(env_backup)
                # Always ensure API key is set
                os.environ["OPENAI_API_KEY"] = API_KEY
            
            try:
                self.llm = ChatOpenAI(
                    model="gpt-3.5-turbo",
                    temperature=0.7
                )
            except Exception:
                self.llm = ChatOpenAI(temperature=0.7)
        
        self.vectorstore = None
        self.qa_chain = None
        
    def load_vectorstore(self):
        """Load existing vector store"""
        # Initialize embeddings if they were delayed
        if self.embeddings is None:
            try:
                # Try to initialize with API key from environment
                if hasattr(self, '_api_key'):
                    os.environ["OPENAI_API_KEY"] = self._api_key
                # Try with model parameter to avoid validation issues
                self.embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
            except Exception:
                # If still fails, try without model
                try:
                    self.embeddings = OpenAIEmbeddings()
                except Exception:
                    return False
        
        if os.path.exists(FAISS_INDEX_PATH) and os.path.exists(FAISS_PKL_PATH):
            try:
                self.vectorstore = FAISS.load_local(
                    PERSIST_DIRECTORY,
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
                return True
            except:
                return False
        return False
    
    def setup_qa_chain(self):
        """Setup the question-answering chain"""
        if self.vectorstore is None:
            return False
        
        retriever = self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 4}
        )
        
        # Custom prompt for natural responses
        prompt_template = """Use the following pieces of context from Jana's resume to answer the question. 
Provide a clear, natural, and conversational answer in your own words. Don't just copy text verbatim - synthesize the information and explain it naturally.
If you don't know the answer based on the context, say so.

Context: {context}

Question: {question}

Answer in a natural, conversational way:"""
        
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
            if not question or len(question.strip()) == 0:
                return "Please ask a question about Jana."
            
            result = self.qa_chain.invoke({"query": question})
            
            if result and "result" in result:
                return result["result"]
            else:
                return "I couldn't generate a response. Please try rephrasing your question."
        except Exception as e:
            error_msg = str(e)
            if "api" in error_msg.lower() or "openai" in error_msg.lower():
                return f"API Error: {error_msg}. Please check your API key."
            return f"Error processing question: {error_msg}"

def main():
    st.set_page_config(
        page_title="Jana's Bot",
        page_icon="💬",
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
    
    # Clean, user-friendly styling
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
        
        /* Input */
        .stTextInput > div > div > input {
            border-color: #ffb6c1;
            border-radius: 10px;
            color: #c2185b !important;
        }
        
        .stTextInput label {
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
    </style>
    """, unsafe_allow_html=True)
    
    st.title("Jana's Bot")
    st.markdown("Ask me anything about Jana!")
    
    # Initialize chatbot
    if "user_bot" not in st.session_state:
        st.session_state.user_bot = UserChatBot()
        if st.session_state.user_bot.load_vectorstore():
            if st.session_state.user_bot.setup_qa_chain():
                st.session_state.bot_ready = True
            else:
                st.session_state.bot_ready = False
        else:
            st.session_state.bot_ready = False
    
    # Check if bot is ready
    if not st.session_state.bot_ready:
        st.error("⚠️ Resume not loaded. Please contact the administrator to load Jana's resume first.")
        st.stop()
    
    # Chat interface
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Hello! I'm Jana's Bot. I can answer questions about Jana's background, experience, skills, education, and qualifications. What would you like to know?"
        })
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me about Jana..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        # Get bot response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = st.session_state.user_bot.get_response(prompt)
                    if response is None or response == "":
                        response = "I'm sorry, I couldn't generate a response. Please try rephrasing your question."
                except Exception as e:
                    response = f"Error: {str(e)}. Please try again."
            
            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()

