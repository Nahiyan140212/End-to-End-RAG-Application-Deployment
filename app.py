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
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .chat-container {
        background: #f8f9fa;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .assistant-message {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border: 1px solid #e9ecef;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .sidebar-info {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 1rem;
    }
    
    .stTextInput > div > div > input {
        border-radius: 25px;
        border: 2px solid #667eea;
        padding: 0.75rem 1rem;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 25px;
        border: none;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .stApp {
    max-width: 100%;
    height: 100%;
    overflow: auto;
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

# Sidebar
with st.sidebar:
    st.markdown("""
    <div class="sidebar-info">
        <h3>🤖 About This Assistant</h3>
        <p>I'm Nahiyan's personal AI assistant, trained on information about him. Ask me anything!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Session metrics
    st.subheader("📊 Session Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Queries", st.session_state.total_queries)
    with col2:
        session_duration = datetime.now() - st.session_state.session_start
        st.metric("Duration", f"{session_duration.seconds//60}m")
    
    # Sample questions
    st.subheader("💡 Sample Questions")
    sample_questions = [
        "What is Nahiyan's background?",
        "What are his skills?",
        "What projects has he worked on?",
        "What are his interests?",
        "How can I contact him?"
    ]
    
    for question in sample_questions:
        if st.button(question, key=f"sample_{question}", use_container_width=True):
            st.session_state.current_query = question
    
    # Clear chat history
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.total_queries = 0
        st.rerun()

# Main content
st.markdown("""
<div class="main-header">
    <h1>🤖 Nahiyan's Personal AI Assistant</h1>
    <p>Ask me anything about Nahiyan - his background, skills, projects, and more!</p>
</div>
""", unsafe_allow_html=True)

# Query input
col1, col2 = st.columns([4, 1])
with col1:
    query = st.text_input(
        "What would you like to know about Nahiyan?",
        placeholder="e.g., What are Nahiyan's technical skills?",
        key="main_query",
        value=st.session_state.get('current_query', '')
    )
with col2:
    ask_button = st.button("Ask 🚀", use_container_width=True)

# Clear the sample query after setting it
if 'current_query' in st.session_state:
    del st.session_state.current_query

# Process query
if (query and ask_button) or (query and st.session_state.get('auto_submit', False)):
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
            
        except Exception as e:
            st.error(f"⚠️ An error occurred: {str(e)}")
            st.info("Please try rephrasing your question or contact support if the issue persists.")

# Display chat history
if st.session_state.chat_history:
    st.subheader("💬 Conversation History")
    
    for i, chat in enumerate(reversed(st.session_state.chat_history)):
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
            <strong>🤖 Nahiyan's Assistant:</strong><br>
            {chat['response']}
        </div>
        """, unsafe_allow_html=True)
        
        # Retrieved chunks (collapsible)
        with st.expander(f"📚 Sources & Context (Query #{len(st.session_state.chat_history)-i})", expanded=False):
            st.markdown("**Retrieved Information Chunks:**")
            for j, chunk in enumerate(chat['chunks'], 1):
                st.markdown(f"""
                <div style="background: #f8f9fa; padding: 0.75rem; margin: 0.5rem 0; border-radius: 8px; border-left: 3px solid #667eea;">
                    <strong>Source {j}:</strong><br>
                    {chunk}
                </div>
                """, unsafe_allow_html=True)
        
        # Add separator
        if i < len(st.session_state.chat_history) - 1:
            st.markdown("---")

# Footer information
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="metric-card">
        <h4>🎯 Accuracy</h4>
        <p>Powered by RAG technology for precise answers</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <h4>⚡ Fast</h4>
        <p>Quick retrieval from Nahiyan's knowledge base</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <h4>🔄 Updated</h4>
        <p>Always current with latest information</p>
    </div>
    """, unsafe_allow_html=True)

# Tips section
with st.expander("💡 Tips for Better Results"):
    st.markdown("""
    **How to get the best answers:**
    
    - **Be specific**: Instead of "Tell me about Nahiyan", try "What programming languages does Nahiyan know?"
    - **Ask follow-ups**: Build on previous answers for deeper insights
    - **Use context**: Reference his projects, skills, or experiences
    - **Try different angles**: Ask about the same topic in different ways
    
    **Example great questions:**
    - "What machine learning projects has Nahiyan worked on?"
    - "How can I collaborate with Nahiyan on a project?"
    - "What makes Nahiyan's approach to software development unique?"
    """)

# Auto-submit functionality (optional)
if query and not ask_button:
    st.session_state.auto_submit = False
