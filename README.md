# End-to-End RAG Application

A comprehensive Retrieval-Augmented Generation (RAG) application that combines document retrieval with AI-powered text generation to provide intelligent question-answering capabilities.

##  Features

- **Document Processing**: Advanced text chunking and preprocessing
- **Vector Storage**: FAISS-based vector database for efficient similarity search
- **Embedding Generation**: State-of-the-art text embeddings for semantic search
- **Intelligent Retrieval**: Context-aware document retrieval system
- **AI-Powered Completion**: Integration with large language models for response generation
- **End-to-End Pipeline**: Seamless integration from document ingestion to answer generation

## 📁 Project Structure

```
End-to-End-RAG-Application/
├── data/                    # Data storage directory
├── faiss_store/            # FAISS vector database storage
├── utils/                  # Core utility modules
│   ├── chunking.py         # Document chunking and preprocessing
│   ├── completion.py       # AI completion and response generation
│   ├── embedding.py        # Text embedding generation
│   ├── prompt.py           # Prompt engineering and templates
│   └── retrieval.py        # Document retrieval and search
├── app.py                  # Main application entry point
├── requirements.txt        # Python dependencies
└── README.md              # Project documentation
```

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/End-to-End-RAG-Application.git
   cd End-to-End-RAG-Application
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory and add necessary API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   # Add other required environment variables
   ```

## 🚀 Quick Start

1. **Run the application**
   ```bash
   python app.py
   ```

2. **Add your documents**
   Place your documents in the `data/` directory

3. **Start querying**
   The application will process your documents and allow you to ask questions

##  Usage

### Document Processing
The application automatically processes documents placed in the `data/` directory, chunking them into manageable pieces and generating embeddings for semantic search.

### Querying
Once documents are processed, you can ask questions and the RAG system will:
1. Retrieve relevant document chunks
2. Generate contextually appropriate responses
3. Provide source attribution

### Example Query Flow
```python
# Example usage (if using programmatically)
from utils.retrieval import retrieve_documents
from utils.completion import generate_response

# Retrieve relevant documents
docs = retrieve_documents("What is the main topic discussed?")

# Generate response
response = generate_response(docs, "What is the main topic discussed?")
print(response)
```

##  Configuration

### Chunking Parameters
Modify chunking behavior in `utils/chunking.py`:
- Chunk size
- Overlap percentage
- Splitting strategy

### Embedding Models
Configure embedding models in `utils/embedding.py`:
- Model selection
- Batch processing
- Dimension settings

### Retrieval Settings
Adjust retrieval parameters in `utils/retrieval.py`:
- Number of retrieved documents
- Similarity thresholds
- Search algorithms

##  Core Components

### Chunking Module (`utils/chunking.py`)
Handles document preprocessing and intelligent text chunking to optimize retrieval performance.

### Embedding Module (`utils/embedding.py`)
Generates high-quality text embeddings using state-of-the-art models for semantic similarity search.

### Retrieval Module (`utils/retrieval.py`)
Implements efficient document retrieval using FAISS vector database with configurable search parameters.

### Completion Module (`utils/completion.py`)
Integrates with language models to generate contextually appropriate responses based on retrieved documents.

### Prompt Module (`utils/prompt.py`)
Contains prompt templates and engineering logic for optimal AI model interactions.

##  Performance Optimization

- **Vector Database**: FAISS provides fast similarity search
- **Batch Processing**: Efficient handling of multiple documents
- **Caching**: Smart caching mechanisms to reduce computation
- **Parallel Processing**: Multi-threaded document processing

## 🔍 Troubleshooting

### Common Issues

1. **Missing Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **API Key Issues**
   Ensure all required API keys are set in your environment variables

3. **Memory Issues**
   Adjust chunk sizes and batch processing parameters for large documents

4. **FAISS Installation**
   If FAISS installation fails, try:
   ```bash
   pip install faiss-cpu  # For CPU-only version
   # or
   pip install faiss-gpu  # For GPU version
   ```

##  Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- FAISS for efficient similarity search
- OpenAI for language model capabilities
- The open-source community for various utilities and libraries

##  Support

For questions, issues, or contributions, please:
- Open an issue on GitHub
- Contact the maintainers
- Check the documentation

---

**Note**: This RAG application is designed for educational and research purposes. Ensure you comply with all relevant terms of service when using external APIs and models.
