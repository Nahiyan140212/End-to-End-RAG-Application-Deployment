import streamlit as st
import time
import json
from urllib.parse import parse_qs
from datetime import datetime
from utils.embedding import get_embedding
from utils.chunking import chunk_text
from utils.retrieval import load_faiss_index, retrieve_chunks
from utils.prompt import build_prompt
from utils.completion import generate_completion

# API endpoint handlers
def handle_api_request():
    """Handle API requests from external applications"""
    try:
        # Get query parameters
        query_params = st.experimental_get_query_params()
        
        # Check if this is an API request
        if 'api' in query_params:
            api_type = query_params['api'][0]
            
            if api_type == 'health':
                # Health check endpoint
                st.json({
                    "status": "healthy",
                    "timestamp": datetime.now().isoformat(),
                    "service": "Nahiyan AI Assistant"
                })
                st.stop()
            
            elif api_type == 'chat':
                # Chat endpoint
                if st.experimental_get_query_params().get('message'):
                    message = st.experimental_get_query_params()['message'][0]
                    
                    # Process the message using your existing RAG system
                    try:
                        index, chunk_mapping = load_faiss_index()
                        top_chunks = retrieve_chunks(message, index, chunk_mapping)
                        prompt = build_prompt(top_chunks, message)
                        response = generate_completion(prompt)
                        
                        # Return JSON response
                        st.json({
                            "response": response,
                            "status": "success",
                            "timestamp": datetime.now().isoformat()
                        })
                        st.stop()
                        
                    except Exception as e:
                        st.json({
                            "error": str(e),
                            "status": "error",
                            "timestamp": datetime.now().isoformat()
                        })
                        st.stop()
    except Exception as e:
        # If there's any error in API handling, continue with normal app
        pass

# Handle API requests first
handle_api_request()



# Page configuration
st.set_page_config(
    page_title="Nahiyan's AI Assistant",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for mobile-friendly dark theme
st.markdown("""
<style>
    /* Base styles */
    .stApp {
        background-color: #1a1a1a;
        color: #ffffff;
        max-width: 100% !important;
        padding: 0 !important;
    }
    
    .main .block-container {
        padding: 1rem !important;
        max-width: 100% !important;
    }
    
    /* Header */
    .main-header {
        background: linear-gradient(135deg, #2d3748, #4a5568);
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        text-align: center;
        color: #ffffff;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    
    .main-header h1 {
        font-size: 1.8rem;
        margin-bottom: 0.5rem;
        color: #ffffff;
        font-weight: bold;
    }
    
    .main-header p {
        font-size: 1rem;
        margin: 0;
        color: #e2e8f0;
    }
    
    /* Example questions */
    .example-section {
        background: #2d3748;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 1px solid #4a5568;
    }
    
    .example-section h3 {
        color: #63b3ed;
        margin-bottom: 1rem;
        font-size: 1.1rem;
        text-align: center;
    }
    
    /* Input section */
    .query-section {
        background: #2d3748;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 1px solid #4a5568;
    }
    
    /* Streamlit input styling */
    .stTextInput > div > div > input {
        background-color: #1a202c !important;
        color: #ffffff !important;
        border: 2px solid #4a5568 !important;
        border-radius: 8px !important;
        padding: 0.75rem !important;
        font-size: 1rem !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #63b3ed !important;
        box-shadow: 0 0 0 2px rgba(99, 179, 237, 0.2) !important;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #3182ce !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: bold !important;
        width: 100% !important;
        margin: 0.25rem 0 !important;
    }
    
    .stButton > button:hover {
        background-color: #2c5282 !important;
    }
    
    /* Messages */
    .user-message {
        background: #3182ce;
        color: #ffffff;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    }
    
    .assistant-message {
        background: #2d3748;
        color: #ffffff;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 1px solid #4a5568;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    }
    
    /* Source styling */
    .source-item {
        background: #1a202c;
        color: #e2e8f0;
        padding: 0.75rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 3px solid #63b3ed;
        font-size: 0.9rem;
    }
    
    /* Stats */
    .stats-bar {
        background: #2d3748;
        padding: 0.75rem;
        border-radius: 8px;
        text-align: center;
        color: #e2e8f0;
        font-size: 0.9rem;
        margin: 1rem 0;
    }
    
    /* Feature cards */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .feature-card {
        background: #2d3748;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        border: 1px solid #4a5568;
        color: #ffffff;
    }
    
    .feature-card h4 {
        color: #63b3ed;
        margin-bottom: 0.5rem;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #2d3748 !important;
        color: #ffffff !important;
        border: 1px solid #4a5568 !important;
    }
    
    .streamlit-expanderContent {
        background-color: #1a202c !important;
        color: #ffffff !important;
        border: 1px solid #4a5568 !important;
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 0.5rem !important;
        }
        
        .main-header {
            padding: 1rem;
        }
        
        .main-header h1 {
            font-size: 1.5rem;
        }
        
        .main-header p {
            font-size: 0.9rem;
        }
        
        .query-section, .example-section {
            padding: 1rem;
        }
        
        .feature-grid {
            grid-template-columns: 1fr;
        }
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Progress bar */
    .stProgress .st-bo {
        background-color: #63b3ed;
    }
    
    /* Spinner */
    .stSpinner {
        color: #63b3ed !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'total_queries' not in st.session_state:
    st.session_state.total_queries = 0
if 'session_start' not in st.session_state:
    st.session_state.session_start = datetime.now()

# Main header
st.markdown("""
<div class="main-header">
    <h1>🤖 Nahiyan's AI Assistant</h1>
    <p>Ask me anything about Nahiyan's background, skills, and projects</p>
</div>
""", unsafe_allow_html=True)

# Example questions
st.markdown("""
<div class="example-section">
    <h3>💡 Popular Questions</h3>
</div>
""", unsafe_allow_html=True)

sample_questions = [
    "What is Nahiyan's background?",
    "What are his technical skills?",
    "What projects has he worked on?",
    "What are his interests?",
    "How can I contact him?"
]

# Create example question buttons
for i, question in enumerate(sample_questions):
    if st.button(question, key=f"sample_{i}"):
        st.session_state.current_query = question
        st.rerun()

# Query input
st.markdown('<div class="query-section">', unsafe_allow_html=True)

# Handle example question clicks
current_query = st.session_state.get('current_query', '')
if current_query:
    st.session_state.pop('current_query', None)
    
    with st.spinner("🔍 Finding information..."):
        try:
            progress_bar = st.progress(0)
            
            # Load and process
            progress_bar.progress(25)
            index, chunk_mapping = load_faiss_index()
            
            progress_bar.progress(50)
            top_chunks = retrieve_chunks(current_query, index, chunk_mapping)
            
            progress_bar.progress(75)
            prompt = build_prompt(top_chunks, current_query)
            response = generate_completion(prompt)
            
            progress_bar.progress(100)
            time.sleep(0.3)
            progress_bar.empty()
            
            # Add to history
            st.session_state.chat_history.append({
                'query': current_query,
                'response': response,
                'chunks': top_chunks,
                'timestamp': datetime.now().strftime("%H:%M")
            })
            st.session_state.total_queries += 1
            
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Manual input
query = st.text_input(
    "Your question:",
    placeholder="Type your question here...",
    key="main_query"
)

if st.button("Ask 🚀"):
    if query:
        with st.spinner("🔍 Finding information..."):
            try:
                progress_bar = st.progress(0)
                
                progress_bar.progress(25)
                index, chunk_mapping = load_faiss_index()
                
                progress_bar.progress(50)
                top_chunks = retrieve_chunks(query, index, chunk_mapping)
                
                progress_bar.progress(75)
                prompt = build_prompt(top_chunks, query)
                response = generate_completion(prompt)
                
                progress_bar.progress(100)
                time.sleep(0.3)
                progress_bar.empty()
                
                # Add to history
                st.session_state.chat_history.append({
                    'query': query,
                    'response': response,
                    'chunks': top_chunks,
                    'timestamp': datetime.now().strftime("%H:%M")
                })
                st.session_state.total_queries += 1
                
                # Clear input
                st.session_state.main_query = ""
                st.rerun()
                
            except Exception as e:
                st.error(f"Error: {str(e)}")

st.markdown('</div>', unsafe_allow_html=True)

# Chat history
if st.session_state.chat_history:
    st.markdown("### 💬 Conversation")
    
    for chat in reversed(st.session_state.chat_history[-3:]):  # Show last 3 conversations
        # User message
        st.markdown(f"""
        <div class="user-message">
            <strong>You ({chat['timestamp']}):</strong><br>
            {chat['query']}
        </div>
        """, unsafe_allow_html=True)
        
        # Assistant response
        st.markdown(f"""
        <div class="assistant-message">
            <strong>🤖 Assistant:</strong><br>
            {chat['response']}
        </div>
        """, unsafe_allow_html=True)
        
        # Sources
        if chat['chunks']:
            with st.expander("📚 View Sources"):
                for j, chunk in enumerate(chat['chunks'][:2], 1):  # Show max 2 sources
                    st.markdown(f"""
                    <div class="source-item">
                        <strong>Source {j}:</strong><br>
                        {chunk[:200]}...
                    </div>
                    """, unsafe_allow_html=True)

# Session stats
if st.session_state.total_queries > 0:
    duration = (datetime.now() - st.session_state.session_start).seconds // 60
    st.markdown(f"""
    <div class="stats-bar">
        📊 {st.session_state.total_queries} questions asked • {duration}m session
    </div>
    """, unsafe_allow_html=True)

# Features
st.markdown("""
<div class="feature-grid">
    <div class="feature-card">
        <h4>🎯 Accurate</h4>
        <p>AI-powered responses based on Nahiyan's information</p>
    </div>
    <div class="feature-card">
        <h4>⚡ Fast</h4>
        <p>Quick search and response generation</p>
    </div>
    <div class="feature-card">
        <h4>🔄 Updated</h4>
        <p>Current information from knowledge base</p>
    </div>
</div>
""", unsafe_allow_html=True)

# JavaScript for Enter key
st.markdown("""
<script>
document.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && e.target.tagName === 'INPUT') {
        const buttons = document.querySelectorAll('button');
        const askButton = Array.from(buttons).find(b => b.textContent.includes('Ask'));
        if (askButton) askButton.click();
    }
});
</script>
""", unsafe_allow_html=True)
