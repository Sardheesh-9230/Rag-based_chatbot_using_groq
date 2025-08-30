🤖 DocuBot - Modern RAG chatbot with ChatGPT-like smooth typewriter interface. Upload documents, ask questions, get intelligent AI responses with beautiful animations.

# RAG Chatbot with FAISS, Pickle, and Groq LLM

# 🤖 DocuBot - Intelligent Document Q&A System

A modern **Retrieval-Augmented Generation (RAG)** chatbot built with Flask, featuring a **ChatGPT-like smooth typewriter interface** for interactive document-based question answering.

## ✨ Features

### 🎯 **Core Capabilities**
- **Document Upload & Processing** - Supports PDF and TXT files
- **Intelligent Vector Search** - FAISS-powered semantic document retrieval
- **LLM Integration** - Groq API for high-quality response generation
- **Context-Aware Responses** - Answers based on your uploaded documents

### 🎨 **Modern UI/UX**
- **ChatGPT-Style Interface** - Smooth, responsive chat experience
- **Typewriter Animation** - Word-by-word text rendering with natural pauses
- **Real-time Typing Indicators** - Animated dots while processing
- **Mobile-Responsive Design** - Works seamlessly across devices

### 🚀 **Technical Stack**
- **Backend**: Flask, Python 3.8+
- **AI/ML**: LangChain, Sentence Transformers, FAISS
- **LLM**: Groq API (Llama models)
- **Frontend**: Vanilla JavaScript, CSS3 Animations
- **Document Processing**: PyPDF2, Text extraction

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- Groq API key ([Get one here](https://groq.com))

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/docubot.git
   cd docubot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Create .env file
   echo "GROQ_API_KEY=your_groq_api_key_here" > .env
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

## 🎮 Usage

### 1. **Upload Documents**
- Click "Choose Files" to upload PDF or TXT documents
- Support for multiple file uploads
- Automatic text extraction and processing

### 2. **Build Vector Index**
- Click "Process Documents" to create searchable index
- Uses Sentence Transformers for embeddings
- FAISS for efficient similarity search

### 3. **Start Chatting**
- Ask questions about your documents
- Get intelligent, context-aware responses
- Enjoy smooth typewriter animations

### 4. **Example Queries**
```
"What are the main points discussed in the document?"
"Summarize the key findings from the research paper"
"What does the document say about [specific topic]?"
```

## 🏗️ Project Structure

```
docubot/
├── app.py                    # Flask web application
├── chatbot.py               # RAG chatbot core logic
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables
├── utils/
│   ├── document_processor.py  # PDF/TXT processing
│   ├── llm.py                 # Groq LLM integration
│   └── retriever.py           # FAISS retrieval system
├── static/
│   ├── chat.css              # Modern UI styling
│   └── chat.js               # Smooth animations & API calls
├── templates/
│   ├── index.html            # File upload interface
│   └── chat.html             # Chat interface
└── data/                     # Document storage directory
```

## 🎨 Key Features Showcase

### Smooth Typewriter Effect
- **Word-by-word rendering** for natural reading experience
- **Variable speed timing** - pauses at punctuation, faster for short words
- **Blinking cursor animation** that disappears when complete
- **Smooth scrolling** that follows text as it appears

### Intelligent Document Processing
- **Chunked text processing** for optimal retrieval
- **Semantic embeddings** using Sentence Transformers
- **Efficient vector search** with FAISS indexing
- **Context-aware responses** from Groq LLM

### Modern Web Interface
- **Responsive design** that works on all devices
- **Gradient backgrounds** and smooth animations
- **Professional typography** with system fonts
- **Accessible UI** with proper contrast and spacing

## 🔧 Configuration

### Environment Variables
```bash
GROQ_API_KEY=your_groq_api_key_here
```

### Customization Options
- **LLM Model**: Change in `utils/llm.py` (default: llama3-8b-8192)
- **Embedding Model**: Modify in `chatbot.py` (default: all-MiniLM-L6-v2)
- **Animation Speed**: Adjust timing in `static/chat.js`
- **UI Theme**: Customize colors in `static/chat.css`

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment
- Use a WSGI server like Gunicorn
- Set up reverse proxy with Nginx
- Configure environment variables
- Enable HTTPS for security

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **LangChain** for the RAG framework
- **Groq** for lightning-fast LLM inference
- **FAISS** for efficient vector search
- **Sentence Transformers** for quality embeddings

## 📞 Support

If you encounter any issues or have questions:
- 🐛 [Report bugs]
- 💡 [Request features]
- 📧 Contact:sardheeshmuthusamy@gmail.com

---

⭐ **Star this repository** if you found it helpful!

**Made with ❤️ and AI**

## Features

- Process and index documents from a directory (PDFs and text files)
- User-friendly web interface for document uploads
- Split documents into smaller chunks for better retrieval
- Create vector embeddings using SentenceTransformer
- Build and store a FAISS vector index
- Retrieve relevant documents based on queries
- Generate responses using Groq LLM
- Interactive chat interface

## Project Structure

```
├── data/                 # Directory for your documents
├── static/               # Static files for web interface
├── templates/            # HTML templates for web interface
├── utils/                # Utility modules
│   ├── document_processor.py  # Document processing utilities
│   ├── retriever.py      # Document retrieval using FAISS
│   ├── llm.py            # Groq LLM interface
├── app.py                # Web interface for document uploads
├── chatbot.py            # Main chatbot application
├── build_index.py        # Script to build the document index
├── process_pdf.py        # Script to process documents
├── run.bat               # Windows launcher script
├── run.sh                # Unix/Linux launcher script
├── requirements.txt      # Python dependencies
└── .env                  # Environment variables for API keys
```

## Setup

1. Clone this repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up your API keys in the `.env` file:

```
GROQ_API_KEY=your_groq_api_key_here
```

## Usage

### Quick Start

Run the launcher script to access all features:

- Windows: `run.bat`
- Linux/Mac: `./run.sh` (you might need to run `chmod +x run.sh` first)

The launcher provides options to:
1. Start the web interface for document uploads
2. Start the chatbot
3. Process documents and build the index
4. Exit

### Method 1: Using the Web Interface

1. Start the web interface:
```bash
python app.py
```

2. Open your browser and go to http://localhost:5000

3. Upload your PDF or text files using the interface

4. Click "Process Documents & Build Vector Index" button

5. Once the index is built, you can start the chatbot either from the web interface or using the command below

### Method 2: Using Command Line

1. Add your documents:
   - Place your PDF and text files in the `data` directory

2. Build the index:
```bash
python process_pdf.py
```

3. Start the chatbot:
```bash
python chatbot.py
```

4. Chat with your documents:
   - Type your questions in the terminal
   - Type 'exit' to quit

## Customization

You can customize the behavior of the RAG chatbot by modifying the following parameters in `chatbot.py`:

- `data_dir`: Directory containing your documents
- `embedding_model`: SentenceTransformer model for embeddings
- `groq_model`: Groq LLM model name
- `top_k`: Number of most similar documents to retrieve

## Dependencies

- groq: Groq LLM API
- faiss-cpu: Vector similarity search
- langchain and langchain-groq: LLM orchestration
- sentence-transformers: Text embeddings
- flask: Web interface
- pypdf2: PDF processing
- numpy: Numerical operations
- pandas: Data manipulation
- pickle-mixin: Object serialization
- python-dotenv: Environment variable management
- werkzeug: File handling utilities

## Web Interface Features

The web interface provides a user-friendly way to:

- Upload multiple PDF and text files
- View and manage uploaded documents
- Process documents and build the vector index
- Launch the chatbot directly from the interface
- See real-time status of documents and index

![Web Interface Screenshot](static/web_interface.png)
