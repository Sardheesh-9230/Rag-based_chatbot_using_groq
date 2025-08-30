import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GroqLLM:
    def __init__(self, model_name="llama3-70b-8192"):
        """
        Initialize the Groq LLM interface
        
        Args:
            model_name: The Groq model to use
        """
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        
        if not self.groq_api_key:
            raise ValueError("GROQ_API_KEY environment variable not set")
        
        self.llm = ChatGroq(
            api_key=self.groq_api_key, 
            model=model_name
        )
        
        # Define the RAG prompt template
        self.prompt_template = ChatPromptTemplate.from_template("""
        You are a helpful AI assistant. Use the following context to answer the user's question.
        If you don't know the answer or can't find it in the context, say so. Don't make up information.
        
        Please structure your response as clear, separate points. Each point should be a complete thought.
        Use bullet points or numbered lists when appropriate to make the information easier to digest.
        
        Context:
        {context}
        
        Question: {query}
        
        Answer:
        """)
        
    def format_context(self, retrieved_documents):
        """Format retrieved documents into a string context"""
        # Join the retrieved document texts with separators
        formatted_docs = []
        
        for i, doc in enumerate(retrieved_documents["texts"]):
            # Add the document text with its source info
            source = retrieved_documents["metadata"][i].get("source", "Unknown source")
            formatted_docs.append(f"Document {i+1} (from {source}):\n{doc}\n")
        
        return "\n".join(formatted_docs)
        
    def create_chain(self):
        """Create a langchain processing chain"""
        chain = (
            {"context": RunnablePassthrough(), 
             "query": RunnablePassthrough()}
            | self.prompt_template
            | self.llm
            | StrOutputParser()
        )
        return chain
        
    def parse_response_to_points(self, response_text):
        """Parse the response into individual points for animated display"""
        import re
        
        # Split by common delimiters and clean up
        points = []
        
        # First, split by bullet points or numbered lists
        bullet_pattern = r'(?:^|\n)(?:[-•*]\s*|\d+\.\s*|[A-Za-z]\.\s*)'
        parts = re.split(bullet_pattern, response_text)
        
        # If no bullet points found, split by sentences or paragraphs
        if len(parts) <= 1:
            # Split by periods followed by space and capital letter, or double newlines
            sentence_pattern = r'(?<=[.!?])\s+(?=[A-Z])|(?:\n\s*\n)'
            parts = re.split(sentence_pattern, response_text)
        
        for part in parts:
            cleaned = part.strip()
            if cleaned and len(cleaned) > 10:  # Filter out very short fragments
                points.append(cleaned)
        
        # If still no good split, return the whole response as one point
        if not points:
            points = [response_text.strip()]
            
        return points

    def generate_response(self, query, retrieved_documents):
        """Generate a response based on the query and retrieved documents"""
        try:
            # Format context from retrieved documents
            context = self.format_context(retrieved_documents)
            
            # Invoke LLM directly with formatted input
            from langchain_core.messages import HumanMessage
            
            prompt = f"""
            You are a helpful AI assistant. Use the following context to answer the user's question.
            If you don't know the answer or can't find it in the context, say so. Don't make up information.
            
            Please structure your response as clear, separate points. Each point should be a complete thought.
            Use bullet points or numbered lists when appropriate to make the information easier to digest.
            
            Context:
            {context}
            
            Question: {query}
            
            Answer:
            """
            
            response = self.llm.invoke([HumanMessage(content=prompt)])
            raw_response = response.content
            
            # Parse response into points for smooth display
            points = self.parse_response_to_points(raw_response)
            
            return {
                'text': raw_response,
                'points': points
            }
        except Exception as e:
            import traceback
            print(f"Error generating response: {str(e)}")
            traceback.print_exc()
            error_msg = f"Sorry, I encountered an error: {str(e)}"
            return {
                'text': error_msg,
                'points': [error_msg]
            }