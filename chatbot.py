from utils.document_processor import DocumentProcessor
from utils.retriever import RAGRetriever
from utils.llm import GroqLLM
import os
import sys

class RAGChatbot:
    def __init__(
        self,
        data_dir="./data",
        index_file="faiss_index.pkl", 
        data_file="documents_data.pkl",
        embedding_model="all-MiniLM-L6-v2",
        groq_model="llama3-8b-8192",  # Using a smaller model by default
        top_k=5
    ):
        """
        Initialize the RAG chatbot
        
        Args:
            data_dir: Directory containing documents
            index_file: Path to the FAISS index file
            data_file: Path to the document data file
            embedding_model: Name of the SentenceTransformer model
            groq_model: Name of the Groq LLM model
            top_k: Number of documents to retrieve
        """
        self.data_dir = data_dir
        self.index_file = index_file
        self.data_file = data_file
        
        print("Initializing RAG Chatbot...")
        
        # Check if the index and data files exist
        if not (os.path.exists(index_file) and os.path.exists(data_file)):
            print("FAISS index or data file not found. Building index...")
            self.build_index()
        else:
            print(f"Using existing index ({index_file}) and data ({data_file})")
        
        # Initialize the retriever
        print("Initializing retriever...")
        self.retriever = RAGRetriever(
            index_file=index_file,
            data_file=data_file,
            model_name=embedding_model,
            top_k=top_k
        )
        
        # Initialize the LLM
        print("Initializing LLM...")
        self.llm = GroqLLM(model_name=groq_model)
    
    def build_index(self):
        """Build the document index"""
        processor = DocumentProcessor(
            data_dir=self.data_dir
        )
        processor.process_documents()
    
    def chat(self, query):
        """Process a query and return a response"""
        # Retrieve relevant documents
        retrieved_docs = self.retriever.retrieve(query)
        
        # Generate response using the LLM
        response_data = self.llm.generate_response(query, retrieved_docs)
        
        return {
            "query": query,
            "response": response_data['text'],
            "response_points": response_data['points'],
            "retrieved_documents": retrieved_docs
        }
    
    def interactive_chat(self):
        """Run an interactive chat session"""
        print("RAG Chatbot initialized. Type 'exit' to quit.\n")
        
        while True:
            try:
                query = input("\nYou: ")
                
                if not query.strip():
                    continue
                
                if query.lower() in ["exit", "quit"]:
                    print("Goodbye!")
                    break
                
                print("Retrieving relevant information...")
                result = self.chat(query)
                print("\nChatbot:", result["response"])
                
            except KeyboardInterrupt:
                print("\nSession terminated by user.")
                break
            except Exception as e:
                import traceback
                print(f"Error: {str(e)}")
                traceback.print_exc()


if __name__ == "__main__":
    chatbot = RAGChatbot()
    chatbot.interactive_chat()