import os
try:
    import numpy as np
    from sentence_transformers import SentenceTransformer
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    print("⚠️  sentence-transformers or faiss not installed. Using simple keyword matching.")

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("⚠️  google-generativeai not installed.")

from django.conf import settings


class RAGService:
    """
    Retrieval-Augmented Generation (RAG) Service
    
    Uses FAISS for vector search and Google Generative AI for response generation.
    """
    
    def __init__(self):
        self.model = None
        self.index = None
        self.knowledge_base = []
        self.initialized = False
        
    def initialize(self):
        """Initialize the RAG service with embeddings and FAISS index"""
        if self.initialized:
            return
        
        print("🔧 Initializing RAG Service...")
        
        # Load knowledge base
        self._load_knowledge_base()
        
        if FAISS_AVAILABLE:
            # Initialize embedding model
            print("📦 Loading SentenceTransformer model...")
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            
            # Create embeddings
            print("🧠 Creating embeddings...")
            embeddings = self.model.encode(self.knowledge_base)
            
            # Create FAISS index
            print("📊 Building FAISS index...")
            dimension = embeddings.shape[1]
            self.index = faiss.IndexFlatL2(dimension)
            self.index.add(embeddings.astype('float32'))
            print("✅ FAISS index created")
        else:
            print("⚠️  Using simple keyword search (FAISS not available)")
        
        # Configure Gemini API
        if GEMINI_AVAILABLE:
            api_key = os.getenv('GEMINI_API_KEY')
            if api_key:
                genai.configure(api_key=api_key)
                print("✅ Gemini API configured")
            else:
                print("⚠️  GEMINI_API_KEY not found in environment variables")
        
        print("✅ RAG Service initialized successfully!")
        self.initialized = True
    
    def _load_knowledge_base(self):
        """Load knowledge base from text file"""
        kb_path = os.path.join(settings.BASE_DIR, 'knowledge_base.txt')
        
        if not os.path.exists(kb_path):
            raise FileNotFoundError(f"Knowledge base not found at {kb_path}")
        
        with open(kb_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split into chunks (paragraphs)
        self.knowledge_base = [
            chunk.strip() 
            for chunk in content.split('\n\n') 
            if chunk.strip()
        ]
        
        print(f"📚 Loaded {len(self.knowledge_base)} chunks from knowledge base")
    
    def _search_faiss(self, query, top_k=3):
        """Search FAISS index for relevant context"""
        if not self.initialized:
            self.initialize()
        
        if FAISS_AVAILABLE and self.index is not None:
            # Encode query
            query_embedding = self.model.encode([query])
            
            # Search FAISS index
            distances, indices = self.index.search(
                query_embedding.astype('float32'), 
                top_k
            )
            
            # Get relevant chunks
            relevant_chunks = [
                self.knowledge_base[idx] 
                for idx in indices[0] 
                if idx < len(self.knowledge_base)
            ]
        else:
            # Fallback: Simple keyword matching
            relevant_chunks = self._simple_search(query, top_k)
        
        return relevant_chunks
    
    def _simple_search(self, query, top_k=3):
        """Simple keyword-based search fallback"""
        query_lower = query.lower()
        query_words = set(query_lower.split())
        
        # Score each chunk by keyword overlap
        scored_chunks = []
        for chunk in self.knowledge_base:
            chunk_lower = chunk.lower()
            chunk_words = set(chunk_lower.split())
            
            # Calculate overlap score
            overlap = len(query_words & chunk_words)
            if overlap > 0 or any(word in chunk_lower for word in query_words):
                scored_chunks.append((chunk, overlap))
        
        # Sort by score and return top K
        scored_chunks.sort(key=lambda x: x[1], reverse=True)
        return [chunk for chunk, score in scored_chunks[:top_k]]
    
    def _construct_prompt(self, query, context_chunks):
        """Construct prompt with context for the LLM"""
        context = "\n\n".join(context_chunks)
        
        prompt = f"""You are a helpful AI assistant. Use the following context to answer the question. If the answer is not in the context, say so and provide a general answer.

Context:
{context}

Question: {query}

Answer:"""
        
        return prompt
    
    def _call_gemini(self, prompt):
        """Call Google Gemini API to get response"""
        if not GEMINI_AVAILABLE:
            # Fallback: Return context-based response
            return "Gemini API not available. Based on the knowledge base: " + prompt.split("Context:")[1].split("Question:")[0][:500] if "Context:" in prompt else "AI service not configured."
        
        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"❌ Error calling Gemini API: {str(e)}")
            # Fallback: Extract context from prompt
            if "Context:" in prompt:
                context = prompt.split("Context:")[1].split("Question:")[0].strip()
                return f"Based on available information: {context[:500]}..."
            return "I apologize, but I encountered an error while generating a response. Please ensure GEMINI_API_KEY is configured."
    
    def get_response(self, query):
        """
        Get AI response for a query using RAG
        
        Args:
            query (str): User's question
            
        Returns:
            str: AI-generated response
        """
        if not self.initialized:
            self.initialize()
        
        # Search for relevant context
        context_chunks = self._search_faiss(query, top_k=3)
        
        # Construct prompt with context
        prompt = self._construct_prompt(query, context_chunks)
        
        # Get response from Gemini
        response = self._call_gemini(prompt)
        
        return response


# Global instance
_rag_service_instance = None


def get_rag_service():
    """Get or create RAG service singleton"""
    global _rag_service_instance
    
    if _rag_service_instance is None:
        _rag_service_instance = RAGService()
    
    return _rag_service_instance
