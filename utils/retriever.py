import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

class RAGRetriever:
    def __init__(
        self, 
        index_file="faiss_index.pkl", 
        data_file="documents_data.pkl", 
        model_name="all-MiniLM-L6-v2", 
        top_k=5
    ):
        """
        Initialize the RAG retriever with FAISS index and data
        
        Args:
            index_file: Path to the FAISS index file
            data_file: Path to the document data file
            model_name: Name of the SentenceTransformer model for embeddings
            top_k: Number of most similar documents to retrieve
        """
        self.model = SentenceTransformer(model_name)
        self.top_k = top_k
        
        # Load the FAISS index and document data
        self.index = self.load_index(index_file)
        self.data = self.load_data(data_file)
    
    def load_index(self, index_file):
        """Load the FAISS index from file"""
        with open(index_file, 'rb') as f:
            index = pickle.load(f)
        return index
    
    def load_data(self, data_file):
        """Load the document data from file"""
        with open(data_file, 'rb') as f:
            data = pickle.load(f)
        return data
    
    def retrieve(self, query, return_embeddings=False):
        """
        Retrieve the most relevant documents for a query
        
        Args:
            query: The query text
            return_embeddings: Whether to return document embeddings
            
        Returns:
            A dictionary with retrieved documents and their metadata
        """
        # Create query embedding
        query_embedding = self.model.encode([query])
        
        # Convert to float32 for FAISS
        query_embedding = query_embedding.astype('float32')
        
        # Search the index
        distances, indices = self.index.search(query_embedding, self.top_k)
        
        # Get the corresponding texts and metadata
        retrieved_texts = [self.data["texts"][i] for i in indices[0]]
        retrieved_metadata = [self.data["metadata"][i] for i in indices[0]]
        
        result = {
            "query": query,
            "texts": retrieved_texts,
            "metadata": retrieved_metadata,
            "distances": distances[0].tolist()
        }
        
        if return_embeddings:
            retrieved_embeddings = [self.data["embeddings"][i] for i in indices[0]]
            result["embeddings"] = retrieved_embeddings
        
        return result