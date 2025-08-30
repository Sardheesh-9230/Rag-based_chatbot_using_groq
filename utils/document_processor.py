import os
import pickle
import numpy as np
from typing import List, Dict, Any, Union
from sentence_transformers import SentenceTransformer
import faiss
import glob
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain.docstore.document import Document

class DocumentProcessor:
    def __init__(self, data_dir: str, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the document processor with a data directory and embedding model
        
        Args:
            data_dir: Directory containing documents to process
            model_name: Name of the SentenceTransformer model to use for embeddings
        """
        self.data_dir = data_dir
        self.model = SentenceTransformer(model_name)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
    
    def load_documents(self):
        """Load documents from the data directory"""
        documents = []
        
        # Load text files
        txt_files = glob.glob(os.path.join(self.data_dir, "**/*.txt"), recursive=True)
        for file_path in txt_files:
            loader = TextLoader(file_path)
            documents.extend(loader.load())
        
        # Load PDF files from data directory
        pdf_files_in_data = glob.glob(os.path.join(self.data_dir, "**/*.pdf"), recursive=True)
        for file_path in pdf_files_in_data:
            loader = PyPDFLoader(file_path)
            documents.extend(loader.load())
            
        # Also check for PDF files in the main directory (one level up)
        main_dir = os.path.dirname(self.data_dir)
        pdf_files_in_main = glob.glob(os.path.join(main_dir, "*.pdf"))
        for file_path in pdf_files_in_main:
            loader = PyPDFLoader(file_path)
            documents.extend(loader.load())
        
        print(f"Loaded {len(documents)} document pages from {len(txt_files)} text files and {len(pdf_files_in_data) + len(pdf_files_in_main)} PDF files")
        return documents
    
    def split_documents(self, documents):
        """Split documents into chunks"""
        chunks = self.text_splitter.split_documents(documents)
        print(f"Split into {len(chunks)} chunks")
        return chunks
    
    def create_embeddings(self, chunks):
        """Create embeddings for document chunks"""
        texts = [doc.page_content for doc in chunks]
        metadata = [doc.metadata for doc in chunks]
        
        # Create embeddings
        embeddings = self.model.encode(texts)
        
        return {
            "texts": texts,
            "embeddings": embeddings,
            "metadata": metadata
        }
    
    def build_faiss_index(self, embeddings):
        """Build a FAISS index from embeddings"""
        # Convert embeddings to float32 numpy array
        embedding_array = np.array(embeddings).astype('float32')
        
        # Get the dimensionality
        dimension = embedding_array.shape[1]
        
        # Create FAISS index
        index = faiss.IndexFlatL2(dimension)
        
        # Add vectors to the index
        index.add(embedding_array)
        
        return index
    
    def save_index_and_data(self, index, data, index_file="faiss_index.pkl", data_file="documents_data.pkl"):
        """Save the FAISS index and document data to disk"""
        # Save the FAISS index
        with open(index_file, 'wb') as f:
            pickle.dump(index, f)
        
        # Save the document data
        with open(data_file, 'wb') as f:
            pickle.dump(data, f)
        
        print(f"Saved index to {index_file} and data to {data_file}")
    
    def process_documents(self):
        """Process documents from loading to saving the index"""
        documents = self.load_documents()
        chunks = self.split_documents(documents)
        data = self.create_embeddings(chunks)
        index = self.build_faiss_index(data["embeddings"])
        
        self.save_index_and_data(
            index, 
            {
                "texts": data["texts"],
                "metadata": data["metadata"],
                "embeddings": data["embeddings"]
            }
        )
        
        return index, data