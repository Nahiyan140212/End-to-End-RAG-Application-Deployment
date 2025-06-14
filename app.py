import streamlit as st
import time
from datetime import datetime
from utils.embedding import get_embedding
from utils.chunking import chunk_text
from utils.retrieval import load_faiss_index, retrieve_chunks
from utils.prompt import build_prompt
from utils.completion import generate_completion

# Page configuration
st.set_page_config(
    page_title="Nahiyan's AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for dark professional styling
st.markdown("""
<style>
    /* Dark theme base */
    .stApp {
        background-color: #0a0e1a;
        color: #e4e6ea;
    }
    
    .main-header {
        background: linear-gradient(135deg, #1a1d29 0%, #2d3748 50%, #1a202c 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        color: #ffffff;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #64b5f6 0%, #42a5f5 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .query-section {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }
    
    .example-questions {
        background: #1a202c;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1.5rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .example-btn {
        background: linear-gradient(135deg, #374151 0%, #4b5563 100%);
        color: #e5e7eb;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 0.75rem 1.5rem;
        border-radius: 25px;
        margin: 0.5rem;
        cursor: pointer;
        transition: all 0.3s ease;
        display: inline-block;
        text-decoration: none;
        font-size: 0.9rem;
    }
    
    .example-btn:hover {
        background: linear-gradient(135deg, #4b5563 0%, #6b7280 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(66, 165, 245, 0.3);
        border-color: #42a5f5;
        color: #ffffff;
    }
    
    .user-message {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 20px;
        margin: 1.5rem 0;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
        border: 1px solid rgba(59, 130, 246, 0.5);
    }
    
    .assistant-message {
        background: linear-gradient(135deg, #1f2937 0%, #374151 100%);
        color: #e5e7eb;
        padding: 2rem;
        border-radius: 20px;
        margin: 1.5rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    .stTextInput > div > div > input {
        background-color: #1f2937 !important;
        color: #e5e7eb !important;
        border: 2px solid #374151 !important;
        border-radius: 25px !important;
        padding: 1rem 1.5rem !important;
        font-size: 1.1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #42a5f5 !important;
        box-shadow: 0 0 0 2px rgba(66, 165, 245, 0.2) !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%) !important;
        color: white !important;
        border-radius: 25px !important;
        border: none !important;
        padding: 1rem 2.5rem !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4) !important;
    }
    
    .source-chip {
        background: #0f172a;
        color: #94a3b8;
        padding: 0.75rem 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        border-left: 4px solid #3b82f6;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .stats-section {
        background: #111827;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 2rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #1f2937 0%, #374151 100%);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
    }
    
    .stExpander {
        background-color: #1f2937 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 15px !important;
    }
    
    .timestamp {
        color: #9ca3af;
        font-size: 0.9rem;
        opacity: 0.8;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #1f2937;
    }
    ::-webkit-scrollbar-thumb {
        background: #4b5563;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #6b7280;
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
    <p style="font-size: 1.2rem; margin: 0; opacity: 0.9;">Ask me anything about Nahiyan - his background, skills, projects, and more!</p>
</div>
""", unsafe_allow_html=True)

# Example questions section
st.markdown("""
<div class="example-questions">
    <h3 style="color: #42a5f5; margin-bottom: 1rem;">💡 Try asking about:</h3>
    <div style="text-align: center;">
""", unsafe_allow_html=True)

# Sample questions as clickable buttons
sample_questions = [
    "What is Nahiyan's background?",
    "What are his technical skills?",
    "What projects has he worked on?",
    "What are his interests?",
    "How can I contact him?"
]

# Create columns for example questions
cols = st.columns(len(sample_questions))
for i, question in enumerate(sample_questions):
    with cols[i]:
        if st.button(question, key=f"sample_{i}", use_container_width=True):
            st.session_state.current_query = question
            st.rerun()

st.markdown("</div></div>", unsafe_allow_html=True)

# Query input section
st.markdown('<div class="query-section">', unsafe_allow_html=True)

# Handle current query from example buttons
current_query = st.session_state.get('current_query', '')
if current_query:
    st.session_state.pop('current_query', None)
    
    # Process the query immediately
    with st.spinner("🔍 Searching through Nahiyan's information..."):
        try:
            # Add loading progress
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Step 1: Load index
            status_text.text("Loading knowledge base...")
            progress_bar.progress(20)
            index, chunk_mapping = load_faiss_index()
            
            # Step 2: Retrieve chunks
            status_text.text("Finding relevant information...")
            progress_bar.progress(50)
            top_chunks = retrieve_chunks(current_query, index, chunk_mapping)
            
            # Step 3: Build prompt
            status_text.text("Preparing response...")
            progress_bar.progress(70)
            prompt = build_prompt(top_chunks, current_query)
            
            # Step 4: Generate response
            status_text.text("Generating answer...")
            progress_bar.progress(90)
            response = generate_completion(prompt)
            
            # Complete
            progress_bar.progress(100)
            status_text.text("Complete!")
            time.sleep(0.5)
            progress_bar.empty()
            status_text.empty()
            
            # Add to chat history
            st.session_state.chat_history.append({
                'query': current_query,
                'response': response,
                'chunks': top_chunks,
                'timestamp': datetime.now().strftime("%H:%M:%S")
            })
            st.session_state.total_queries += 1
            
        except Exception as e:
            st.error(f"⚠️ An error occurred: {str(e)}")
            st.info("Please try rephrasing your question or contact support if the issue persists.")

# Regular query input
col1, col2 = st.columns([5, 1])
with col1:
    query = st.text_input(
        "",
        placeholder="What would you like to know about Nahiyan?",
        key="main_query",
        label_visibility="collapsed"
    )
with col2:
    ask_button = st.button("Ask 🚀", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Process manual query
if query and (ask_button or st.session_state.get('enter_pressed', False)):
    st.session_state.pop('enter_pressed', None)
    
    with st.spinner("🔍 Searching through Nahiyan's information..."):
        try:
            # Add loading progress
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Step 1: Load index
            status_text.text("Loading knowledge base...")
            progress_bar.progress(20)
            index, chunk_mapping = load_faiss_index()
            
            # Step 2: Retrieve chunks
            status_text.text("Finding relevant information...")
            progress_bar.progress(50)
            top_chunks = retrieve_chunks(query, index, chunk_mapping)
            
            # Step 3: Build prompt
            status_text.text("Preparing response...")
            progress_bar.progress(70)
            prompt = build_prompt(top_chunks, query)
            
            # Step 4: Generate response
            status_text.text("Generating answer...")
            progress_bar.progress(90)
            response = generate_completion(prompt)
            
            # Complete
            progress_bar.progress(100)
            status_text.text("Complete!")
            time.sleep(0.5)
            progress_bar.empty()
            status_text.empty()
            
            # Add to chat history
            st.session_state.chat_history.append({
                'query': query,
                'response': response,
                'chunks': top_chunks,
                'timestamp': datetime.now().strftime("%H:%M:%S")
            })
            st.session_state.total_queries += 1
            
            # Clear the input
            st.session_state.main_query = ""
            
        except Exception as e:
            st.error(f"⚠️ An error occurred: {str(e)}")
            st.info("Please try rephrasing your question or contact support if the issue persists.")

# Display chat history
if st.session_state.chat_history:
    st.markdown("### 💬 Conversation")
    
    for i, chat in enumerate(reversed(st.session_state.chat_history)):
        # User message
        st.markdown(f"""
        <div class="user-message">
            <strong>You</strong> <span class="timestamp">({chat['timestamp']})</span><br><br>
            {chat['query']}
        </div>
        """, unsafe_allow_html=True)
        
        # Assistant response
        st.markdown(f"""
        <div class="assistant-message">
            <strong>🤖 Nahiyan's Assistant</strong><br><br>
            {chat['response']}
        </div>
        """, unsafe_allow_html=True)
        
        # Retrieved chunks (collapsible)
        with st.expander(f"📚 Sources & Context", expanded=False):
            for j, chunk in enumerate(chat['chunks'], 1):
                st.markdown(f"""
                <div class="source-chip">
                    <strong>Source {j}:</strong><br>
                    {chunk}
                </div>
                """, unsafe_allow_html=True)

# Session stats
if st.session_state.total_queries > 0:
    session_duration = datetime.now() - st.session_state.session_start
    st.markdown(f"""
    <div class="stats-section">
        <strong>Session Stats:</strong> {st.session_state.total_queries} queries • {session_duration.seconds//60}m active
        &nbsp;&nbsp;|&nbsp;&nbsp;
        <a href="#" onclick="if(confirm('Clear chat history?')) {{ window.location.reload(); }}" style="color: #f87171; text-decoration: none;">🗑️ Clear History</a>
    </div>
    """, unsafe_allow_html=True)

# Footer features
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="metric-card">
        <h4 style="color: #42a5f5;">🎯 Accurate</h4>
        <p>Powered by RAG technology for precise answers</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <h4 style="color: #42a5f5;">⚡ Fast</h4>
        <p>Quick retrieval from knowledge base</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <h4 style="color: #42a5f5;">🔄 Current</h4>
        <p>Always updated with latest information</p>
    </div>
    """, unsafe_allow_html=True)

# JavaScript for Enter key functionality
st.markdown("""
<script>
document.addEventListener('DOMContentLoaded', function() {
    const input = document.querySelector('input[aria-label=""]');
    if (input) {
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                const button = document.querySelector('button[kind="primary"]');
                if (button) {
                    button.click();
                }
            }
        });
    }
});
</script>
""", unsafe_allow_html=True)
