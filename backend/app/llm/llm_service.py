# """
# LLM and RAG service for conversational data analysis.

# Provides retrieval-augmented generation capabilities for natural language
# querying of ARGO float data with fallback to deterministic responses.
# """

# import os
# import json
# import logging
# from typing import List, Dict, Any, Optional
# from datetime import datetime
# import pandas as pd
# from pathlib import Path

# # Optional imports for full LLM functionality
# try:
#     import openai
#     from sentence_transformers import SentenceTransformer
#     import chromadb
#     FULL_LLM_AVAILABLE = True
# except ImportError:
#     FULL_LLM_AVAILABLE = False
#     logging.warning("LLM dependencies not fully available. Using fallback mode.")

# from ..services.data_service import DataService

# logger = logging.getLogger(__name__)


# class LLMService:
#     """
#     Language model service for conversational data analysis.
    
#     Implements RAG pipeline with vector similarity search and LLM generation.
#     Falls back to rule-based responses when OpenAI API is not configured.
#     """
    
#     def __init__(self):
#         self.data_service = DataService()
#         self.openai_key = os.getenv("OPENAI_API_KEY")
#         self.embed_model_name = os.getenv("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
#         self.vector_db_path = os.getenv("VECTOR_DB_PATH", "./vector_store")
        
#         # Initialize components
#         self.embed_model = None
#         self.vector_store = None
#         self.openai_client = None
        
#         if FULL_LLM_AVAILABLE:
#             self._initialize_llm_components()
        
#         # Pre-built knowledge base for fallback responses
#         self.knowledge_base = self._build_knowledge_base()
    
#     def _initialize_llm_components(self):
#         """Initialize LLM, embedding model, and vector store."""
#         try:
#             # Initialize embedding model
#             self.embed_model = SentenceTransformer(self.embed_model_name)
#             logger.info(f"Loaded embedding model: {self.embed_model_name}")
            
#             # Initialize vector store
#             self.vector_store = chromadb.PersistentClient(path=self.vector_db_path)
#             self.collection = self.vector_store.get_or_create_collection(
#                 name="argo_metadata",
#                 metadata={"description": "ARGO float data metadata and summaries"}
#             )
            
#             # Initialize OpenAI client if API key available
#             if self.openai_key:
#                 self.openai_client = openai.OpenAI(api_key=self.openai_key)
#                 logger.info("OpenAI client initialized")
            
#             # Embed metadata if collection is empty
#             if self.collection.count() == 0:
#                 self._embed_metadata()
                
#         except Exception as e:
#             logger.error(f"Error initializing LLM components: {e}")
#             logger.info("Falling back to deterministic responses")
    
#     def _build_knowledge_base(self) -> Dict[str, Any]:
#         """Build knowledge base for fallback responses."""
#         return {
#             "temperature_info": {
#                 "description": "Sea surface temperature measurements from ARGO floats",
#                 "range": "26-31°C in Indian Ocean surface waters",
#                 "patterns": "Seasonal variation with warmer temperatures in April-May"
#             },
#             "salinity_info": {
#                 "description": "Sea surface salinity measurements", 
#                 "range": "34-36 PSU typical range",
#                 "patterns": "Generally stable with some seasonal variation"
#             },
#             "heat_content_info": {
#                 "description": "Ocean heat content representing thermal energy storage",
#                 "range": "5000-7000 typical values",
#                 "patterns": "Varies by location and season, higher values at 80°E"
#             },
#             "spatial_coverage": {
#                 "latitudes": "Equatorial region (0°)",
#                 "longitudes": "Indian Ocean 60°E to 100°E",
#                 "period": "2010-2013"
#             },
#             "data_availability": {
#                 "surface_timeseries": "High-frequency temperature and salinity",
#                 "monthly_averages": "Depth-resolved monthly climatology", 
#                 "heat_content": "Integrated heat content time series"
#             }
#         }
    
#     def _embed_metadata(self):
#         """Create embeddings for data metadata and summaries."""
#         if not FULL_LLM_AVAILABLE or self.embed_model is None:
#             return
        
#         try:
#             # Create metadata summaries for embedding
#             metadata_docs = [
#                 "ARGO float surface temperature data from Indian Ocean covering 2010-2013 period",
#                 "Sea surface salinity measurements with seasonal variations",
#                 "Ocean heat content representing thermal energy in water column",
#                 "Vertical temperature and salinity profiles by depth",
#                 "Monthly climatological averages for oceanographic analysis",
#                 "Equatorial Indian Ocean data coverage from 60E to 100E longitude",
#                 "Temperature range 26-31 degrees Celsius in surface waters",
#                 "Salinity values typically 34-36 PSU practical salinity units",
#                 "Heat content variations between 5000-7000 energy units"
#             ]
            
#             # Generate embeddings
#             embeddings = self.embed_model.encode(metadata_docs)
            
#             # Store in vector database
#             ids = [f"metadata_{i}" for i in range(len(metadata_docs))]
            
#             self.collection.add(
#                 embeddings=embeddings.tolist(),
#                 documents=metadata_docs,
#                 ids=ids,
#                 metadatas=[{"type": "data_summary", "index": i} for i in range(len(metadata_docs))]
#             )
            
#             logger.info(f"Embedded {len(metadata_docs)} metadata documents")
            
#         except Exception as e:
#             logger.error(f"Error embedding metadata: {e}")
    
#     def retrieve(self, query: str, n_results: int = 3) -> List[Dict[str, Any]]:
#         """
#         Retrieve relevant documents using semantic similarity.
        
#         Args:
#             query: User query text
#             n_results: Number of similar documents to retrieve
            
#         Returns:
#             List of relevant documents with metadata
#         """
#         if not FULL_LLM_AVAILABLE or self.embed_model is None or self.collection is None:
#             # Fallback: simple keyword matching
#             return self._keyword_retrieve(query)
        
#         try:
#             # Generate query embedding
#             query_embedding = self.embed_model.encode([query])
            
#             # Retrieve similar documents
#             results = self.collection.query(
#                 query_embeddings=query_embedding.tolist(),
#                 n_results=n_results
#             )
            
#             retrieved_docs = []
#             for i, doc in enumerate(results['documents'][0]):
#                 retrieved_docs.append({
#                     "content": doc,
#                     "metadata": results['metadatas'][0][i],
#                     "similarity": results['distances'][0][i] if 'distances' in results else 1.0
#                 })
            
#             return retrieved_docs
            
#         except Exception as e:
#             logger.error(f"Error retrieving documents: {e}")
#             return self._keyword_retrieve(query)
    
#     def _keyword_retrieve(self, query: str) -> List[Dict[str, Any]]:
#         """Simple keyword-based retrieval fallback."""
#         query_lower = query.lower()
#         retrieved = []
        
#         # Match query terms to knowledge base
#         if any(word in query_lower for word in ['temperature', 'temp', 'warm', 'cold']):
#             retrieved.append({
#                 "content": "Temperature data shows seasonal variation in Indian Ocean surface waters, ranging from 26-31°C",
#                 "metadata": {"type": "temperature_analysis"},
#                 "similarity": 0.8
#             })
        
#         if any(word in query_lower for word in ['salinity', 'salt']):
#             retrieved.append({
#                 "content": "Salinity measurements show values typically between 34-36 PSU with seasonal patterns",
#                 "metadata": {"type": "salinity_analysis"},
#                 "similarity": 0.8
#             })
        
#         if any(word in query_lower for word in ['heat content', 'thermal', 'energy']):
#             retrieved.append({
#                 "content": "Heat content represents thermal energy storage, varying by location with higher values at 80°E",
#                 "metadata": {"type": "heat_analysis"},
#                 "similarity": 0.8
#             })
        
#         if any(word in query_lower for word in ['location', 'where', 'longitude', 'latitude']):
#             retrieved.append({
#                 "content": "Data coverage spans equatorial Indian Ocean from 60°E to 100°E longitude during 2010-2013",
#                 "metadata": {"type": "spatial_info"},
#                 "similarity": 0.7
#             })
        
#         return retrieved[:3]  # Return top 3 matches
    
#     async def answer_with_context(self, query: str, retrieved_docs: List[Dict[str, Any]]) -> str:
#         """
#         Generate answer using retrieved context and LLM.
        
#         Args:
#             query: User query
#             retrieved_docs: Retrieved relevant documents
            
#         Returns:
#             Generated response string
#         """
#         if self.openai_client is None:
#             return self._generate_fallback_answer(query, retrieved_docs)
        
#         try:
#             # Build context from retrieved documents
#             context = "\n".join([doc["content"] for doc in retrieved_docs])
            
#             # Create prompt for LLM
#             system_prompt = """You are an expert oceanographer analyzing ARGO float data from the Indian Ocean. 
#             Use the provided context to answer questions about ocean temperature, salinity, heat content, and related oceanographic phenomena.
#             Be specific and reference the data when possible. If the context doesn't contain enough information, say so clearly."""
            
#             user_prompt = f"""Context: {context}
            
#             Question: {query}
            
#             Please provide a detailed answer based on the oceanographic data context."""
            
#             # Call OpenAI API
#             response = self.openai_client.chat.completions.create(
#                 model="gpt-3.5-turbo",
#                 messages=[
#                     {"role": "system", "content": system_prompt},
#                     {"role": "user", "content": user_prompt}
#                 ],
#                 max_tokens=500,
#                 temperature=0.3
#             )
            
#             return response.choices[0].message.content.strip()
            
#         except Exception as e:
#             logger.error(f"Error generating LLM response: {e}")
#             return self._generate_fallback_answer(query, retrieved_docs)
    
#     def _generate_fallback_answer(self, query: str, retrieved_docs: List[Dict[str, Any]]) -> str:
#         """Generate deterministic answer without LLM."""
#         query_lower = query.lower()
        
#         # Temperature queries
#         if any(word in query_lower for word in ['temperature', 'temp', 'warm', 'cold']):
#             if '60' in query or '60e' in query_lower:
#                 return ("Based on the data, temperatures at 60°E longitude show seasonal variation. "
#                        "Surface temperatures typically range from 26-31°C, with warmer conditions "
#                        "during April-May period and cooler temperatures in winter months.")
#             elif '80' in query or '80e' in query_lower:
#                 return ("At 80°E longitude, sea surface temperatures follow similar seasonal patterns "
#                        "to 60°E, with typical ranges of 27-30°C. The data shows some year-to-year "
#                        "variability in the timing of maximum temperatures.")
#             else:
#                 return ("Temperature data from Indian Ocean ARGO floats shows seasonal variation "
#                        "with surface temperatures ranging from 26-31°C across the region.")
        
#         # Salinity queries
#         if any(word in query_lower for word in ['salinity', 'salt']):
#             return ("Salinity measurements from the ARGO floats show values typically between "
#                    "34-36 PSU (Practical Salinity Units). There is some seasonal variation "
#                    "and spatial differences across the Indian Ocean region.")
        
#         # Heat content queries
#         if any(word in query_lower for word in ['heat content', 'heat', 'energy']):
#             if 'compare' in query_lower or 'difference' in query_lower:
#                 return ("Heat content shows significant spatial variation across the Indian Ocean. "
#                        "Values at 80°E are generally higher (around 6000-6600 units) compared to "
#                        "60°E (around 5900-6300 units), indicating more thermal energy storage in the eastern region.")
#             else:
#                 return ("Ocean heat content represents the thermal energy stored in the water column. "
#                        "In this dataset, values typically range from 5000-7000 units, with seasonal "
#                        "and spatial variations across the Indian Ocean.")
        
#         # Trend queries
#         if any(word in query_lower for word in ['trend', 'change', 'increase', 'decrease']):
#             return ("The 2010-2013 data shows seasonal patterns rather than clear long-term trends "
#                    "due to the relatively short time period. Longer time series would be needed "
#                    "to identify significant climate trends.")
        
#         # Location queries
#         if any(word in query_lower for word in ['where', 'location', 'longitude', 'latitude']):
#             return ("The dataset covers equatorial Indian Ocean locations primarily at 60°E and 80°E "
#                    "longitude, 0° latitude. Data spans the period from 2010 to 2013 with various "
#                    "measurement types including surface timeseries and depth profiles.")
        
#         # Default response
#         if retrieved_docs:
#             context_summary = ". ".join([doc["content"][:100] + "..." for doc in retrieved_docs[:2]])
#             return f"Based on the available data: {context_summary}"
#         else:
#             return ("I can help you analyze ARGO float data from the Indian Ocean covering temperature, "
#                    "salinity, and heat content measurements from 2010-2013. Could you please specify "
#                    "what aspect of the data you're interested in?")
    
#     async def answer_query(self, query: str) -> str:
#         """
#         Main entry point for answering user queries.
        
#         Args:
#             query: Natural language query from user
            
#         Returns:
#             Generated response based on data and context
#         """
#         try:
#             # Retrieve relevant documents
#             retrieved_docs = self.retrieve(query)
            
#             # Generate answer with context
#             answer = await self.answer_with_context(query, retrieved_docs)
            
#             return answer
            
#         except Exception as e:
#             logger.error(f"Error processing query: {e}")
#             return ("I apologize, but I encountered an error processing your question. "
#                    "Please try rephrasing your query or contact support if the issue persists.")


# def natural_language_to_sql(query: str) -> Dict[str, Any]:
#     """
#     Example MCP-style function for mapping natural language to SQL queries.
    
#     This is a demonstration of how natural language intent can be mapped
#     to structured database queries for oceanographic data.
    
#     TODO: Implement full natural language processing with entity extraction
#     and intent classification for complex oceanographic queries.
#     """
    
#     # Example mappings - in production, use NLP models for intent classification
#     query_lower = query.lower()
    
#     # Temperature query example
#     if 'temperature' in query_lower and 'average' in query_lower:
#         if '2012' in query:
#             return {
#                 "intent": "temperature_average",
#                 "sql": """
#                     SELECT AVG(temperature) as avg_temp, lat, lon
#                     FROM monthly_averages 
#                     WHERE EXTRACT(YEAR FROM time) = 2012 
#                       AND depth = 5.0
#                     GROUP BY lat, lon
#                 """,
#                 "parameters": {"year": 2012, "depth": 5.0},
#                 "description": "Average surface temperature by location for 2012"
#             }
    
#     # Salinity trend example
#     if 'salinity' in query_lower and 'trend' in query_lower:
#         return {
#             "intent": "salinity_trend",
#             "sql": """
#                 SELECT time, temperature, salinity
#                 FROM surface_data 
#                 ORDER BY time
#             """,
#             "parameters": {},
#             "description": "Surface salinity time series for trend analysis"
#         }
    
#     # Heat content comparison example
#     if 'heat content' in query_lower and any(word in query_lower for word in ['compare', 'difference']):
#         return {
#             "intent": "heat_content_comparison",
#             "sql": """
#                 SELECT lon, AVG(heat_content) as avg_heat_content
#                 FROM heat_content
#                 WHERE lat = 0.0
#                 GROUP BY lon
#                 ORDER BY lon
#             """,
#             "parameters": {"lat": 0.0},
#             "description": "Heat content comparison across longitudes"
#         }
    
#     # Default fallback
#     return {
#         "intent": "general_query",
#         "sql": "SELECT * FROM surface_data LIMIT 10",
#         "parameters": {},
#         "description": "General data sample"
#     }


# # Test examples for the MCP-style function
# def test_natural_language_to_sql():
#     """Test cases for natural language to SQL mapping."""
    
#     test_queries = [
#         "What is the average temperature at 60°E in 2012?",
#         "Show me the salinity trends over time",
#         "How does heat content compare between different longitudes?",
#         "What are the typical measurements available?"
#     ]
    
#     expected_intents = [
#         "temperature_average",
#         "salinity_trend", 
#         "heat_content_comparison",
#         "general_query"
#     ]
    
#     print("Testing Natural Language to SQL mapping:")
#     for i, query in enumerate(test_queries):
#         result = natural_language_to_sql(query)
#         print(f"\nQuery: {query}")
#         print(f"Intent: {result['intent']}")
#         print(f"SQL: {result['sql']}")
#         print(f"Expected: {expected_intents[i]} - {'✓' if result['intent'] == expected_intents[i] else '✗'}")


# if __name__ == "__main__":
#     test_natural_language_to_sql()



# import os
# import json
# import logging
# from typing import List, Dict, Any, Optional
# from datetime import datetime
# import pandas as pd
# from pathlib import Path

# # Optional imports for full LLM functionality
# try:
#     from groq import Groq, AsyncGroq
#     from sentence_transformers import SentenceTransformer
#     import chromadb
#     FULL_LLM_AVAILABLE = True
# except ImportError:
#     FULL_LLM_AVAILABLE = False
#     logging.warning("LLM dependencies not fully available. Using fallback mode.")

# from ..services.data_service import DataService

# logger = logging.getLogger(__name__)


# class LLMService:
#     """
#     Language model service for conversational data analysis.
    
#     Implements RAG pipeline with vector similarity search and LLM generation.
#     Falls back to rule-based responses when Groq API is not configured.
#     """
    
#     def __init__(self):
#         self.data_service = DataService()
#         self.groq_api_key = os.getenv("GROQ_API_KEY")
#         self.embed_model_name = os.getenv("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
#         self.vector_db_path = os.getenv("VECTOR_DB_PATH", "./vector_store")
#         self.groq_model = os.getenv("GROQ_MODEL", "llama3-70b-8192")
        
#         # Initialize components
#         self.embed_model = None
#         self.vector_store = None
#         self.groq_client = None
        
#         if FULL_LLM_AVAILABLE:
#             self._initialize_llm_components()
        
#         # Pre-built knowledge base for fallback responses
#         self.knowledge_base = self._build_knowledge_base()
    
#     def _initialize_llm_components(self):
#         """Initialize LLM, embedding model, and vector store."""
#         try:
#             # Initialize embedding model
#             self.embed_model = SentenceTransformer(self.embed_model_name)
#             logger.info(f"Loaded embedding model: {self.embed_model_name}")
            
#             # Initialize vector store
#             self.vector_store = chromadb.PersistentClient(path=self.vector_db_path)
#             self.collection = self.vector_store.get_or_create_collection(
#                 name="argo_metadata",
#                 metadata={"description": "ARGO float data metadata and summaries"}
#             )
            
#             # Initialize Groq client if API key available
#             if self.groq_api_key:
#                 # Use AsyncGroq for asynchronous operations if needed in FastAPI endpoints
#                 self.groq_client = Groq(api_key=self.groq_api_key)
#                 logger.info("Groq client initialized")
            
#             # Embed metadata if collection is empty
#             if self.collection.count() == 0:
#                 self._embed_metadata()
                
#         except Exception as e:
#             logger.error(f"Error initializing LLM components: {e}")
#             logger.info("Falling back to deterministic responses")
    
#     def _build_knowledge_base(self) -> Dict[str, Any]:
#         """Build knowledge base for fallback responses."""
#         return {
#             "temperature_info": {
#                 "description": "Sea surface temperature measurements from ARGO floats",
#                 "range": "26-31°C in Indian Ocean surface waters",
#                 "patterns": "Seasonal variation with warmer temperatures in April-May"
#             },
#             "salinity_info": {
#                 "description": "Sea surface salinity measurements", 
#                 "range": "34-36 PSU typical range",
#                 "patterns": "Generally stable with some seasonal variation"
#             },
#             "heat_content_info": {
#                 "description": "Ocean heat content representing thermal energy storage",
#                 "range": "5000-7000 typical values",
#                 "patterns": "Varies by location and season, higher values at 80°E"
#             },
#             "spatial_coverage": {
#                 "latitudes": "Equatorial region (0°)",
#                 "longitudes": "Indian Ocean 60°E to 100°E",
#                 "period": "2010-2013"
#             },
#             "data_availability": {
#                 "surface_timeseries": "High-frequency temperature and salinity",
#                 "monthly_averages": "Depth-resolved monthly climatology", 
#                 "heat_content": "Integrated heat content time series"
#             }
#         }
    
#     def _embed_metadata(self):
#         """Create embeddings for data metadata and summaries."""
#         if not FULL_LLM_AVAILABLE or self.embed_model is None:
#             return
        
#         try:
#             # Create metadata summaries for embedding
#             metadata_docs = [
#                 "ARGO float surface temperature data from Indian Ocean covering 2010-2013 period",
#                 "Sea surface salinity measurements with seasonal variations",
#                 "Ocean heat content representing thermal energy in water column",
#                 "Vertical temperature and salinity profiles by depth",
#                 "Monthly climatological averages for oceanographic analysis",
#                 "Equatorial Indian Ocean data coverage from 60E to 100E longitude",
#                 "Temperature range 26-31 degrees Celsius in surface waters",
#                 "Salinity values typically 34-36 PSU practical salinity units",
#                 "Heat content variations between 5000-7000 energy units"
#             ]
            
#             # Generate embeddings
#             embeddings = self.embed_model.encode(metadata_docs)
            
#             # Store in vector database
#             ids = [f"metadata_{i}" for i in range(len(metadata_docs))]
            
#             self.collection.add(
#                 embeddings=embeddings.tolist(),
#                 documents=metadata_docs,
#                 ids=ids,
#                 metadatas=[{"type": "data_summary", "index": i} for i in range(len(metadata_docs))]
#             )
            
#             logger.info(f"Embedded {len(metadata_docs)} metadata documents")
            
#         except Exception as e:
#             logger.error(f"Error embedding metadata: {e}")
    
#     def retrieve(self, query: str, n_results: int = 3) -> List[Dict[str, Any]]:
#         """
#         Retrieve relevant documents using semantic similarity.
        
#         Args:
#             query: User query text
#             n_results: Number of similar documents to retrieve
            
#         Returns:
#             List of relevant documents with metadata
#         """
#         if not FULL_LLM_AVAILABLE or self.embed_model is None or self.collection is None:
#             # Fallback: simple keyword matching
#             return self._keyword_retrieve(query)
        
#         try:
#             # Generate query embedding
#             query_embedding = self.embed_model.encode([query])
            
#             # Retrieve similar documents
#             results = self.collection.query(
#                 query_embeddings=query_embedding.tolist(),
#                 n_results=n_results
#             )
            
#             retrieved_docs = []
#             for i, doc in enumerate(results['documents'][0]):
#                 retrieved_docs.append({
#                     "content": doc,
#                     "metadata": results['metadatas'][0][i],
#                     "similarity": results['distances'][0][i] if 'distances' in results else 1.0
#                 })
            
#             return retrieved_docs
            
#         except Exception as e:
#             logger.error(f"Error retrieving documents: {e}")
#             return self._keyword_retrieve(query)

#     async def generate_response(self, query: str, retrieved_docs: List[Dict[str, Any]]) -> str:
#         """
#         Generate a conversational response using the Groq API.
        
#         Args:
#             query: User query text.
#             retrieved_docs: List of documents retrieved from the vector store.
        
#         Returns:
#             Generated response string.
#         """
#         if not self.groq_client:
#             return self._generate_fallback_response(query)
            
#         try:
#             context = "\n".join([doc['content'] for doc in retrieved_docs])
#             prompt = (
#                 f"You are a helpful assistant for oceanographic data analysis. "
#                 f"Based on the following context, answer the user's query.\n\n"
#                 f"Context: {context}\n\n"
#                 f"User: {query}\n\n"
#                 f"Answer:"
#             )
            
#             chat_completion = self.groq_client.chat.completions.create(
#                 messages=[
#                     {
#                         "role": "user",
#                         "content": prompt,
#                     }
#                 ],
#                 model=self.groq_model,
#             )
            
#             return chat_completion.choices[0].message.content
        
#         except Exception as e:
#             logger.error(f"Error generating response with Groq API: {e}")
#             return self._generate_fallback_response(query)
            
#     def _generate_fallback_response(self, query: str) -> str:
#         """Generate a rule-based fallback response."""
#         query_lower = query.lower()
#         if any(word in query_lower for word in ['temperature', 'temp']):
#             return self.knowledge_base['temperature_info']['description'] + ". Range: " + self.knowledge_base['temperature_info']['range']
#         if any(word in query_lower for word in ['salinity', 'salt']):
#             return self.knowledge_base['salinity_info']['description'] + ". Range: " + self.knowledge_base['salinity_info']['range']
#         if any(word in query_lower for word in ['heat content', 'heat']):
#             return self.knowledge_base['heat_content_info']['description'] + ". Range: " + self.knowledge_base['heat_content_info']['range']
#         if any(word in query_lower for word in ['data', 'coverage']):
#             return f"Data covers the Equatorial Indian Ocean from 60E to 100E longitude, between 2010 and 2013."
        
#         return "I'm sorry, I can only provide information based on the pre-configured knowledge base at the moment. Please ask about temperature, salinity, heat content, or data coverage."

#     def _keyword_retrieve(self, query: str) -> List[Dict[str, Any]]:
#         """Simple keyword-based retrieval fallback."""
#         query_lower = query.lower()
#         retrieved = []
        
#         # Match query terms to knowledge base
#         if any(word in query_lower for word in ['temperature', 'temp', 'warm', 'cold']):
#             retrieved.append({
#                 "content": "Temperature data shows seasonal variation in Indian Ocean surface waters, ranging from 26-31°C",
#                 "metadata": {"type": "temperature_analysis"},
#                 "similarity": 0.8
#             })
        
#         if any(word in query_lower for word in ['salinity', 'salt']):
#             retrieved.append({
#                 "content": "Sea surface salinity measurements are typically in the 34-36 PSU range",
#                 "metadata": {"type": "salinity_analysis"},
#                 "similarity": 0.8
#             })
            
#         return retrieved



# import os
# import json
# import logging
# from typing import List, Dict, Any, Optional
# from datetime import datetime
# import pandas as pd
# from pathlib import Path

# # Optional imports for full LLM functionality
# try:
#     from groq import Groq  # Groq SDK
#     from sentence_transformers import SentenceTransformer
#     import chromadb
#     FULL_LLM_AVAILABLE = True
# except ImportError:
#     FULL_LLM_AVAILABLE = False
#     logging.warning("LLM dependencies not fully available. Using fallback mode.")

# from ..services.data_service import DataService

# logger = logging.getLogger(__name__)

# class LLMService:
#     """
#     Language model service for conversational data analysis.

#     Implements RAG pipeline with vector similarity search and Groq chat generation.
#     Falls back to rule-based responses when Groq API is not configured.
#     """

#     def __init__(self):
#         self.data_service = DataService()
#         # Groq configuration
#         self.groq_key = os.getenv("GROQ_API_KEY")
#         self.groq_model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
#         self.embed_model_name = os.getenv("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
#         self.vector_db_path = os.getenv("VECTOR_DB_PATH", "./vector_store")

#         # Initialize components
#         self.embed_model = None
#         self.vector_store = None
#         self.collection = None
#         self.groq_client = None

#         if FULL_LLM_AVAILABLE:
#             self._initialize_llm_components()

#         # Pre-built knowledge base for fallback responses
#         self.knowledge_base = self._build_knowledge_base()

#     def _initialize_llm_components(self):
#         """Initialize embedding model, vector store, and Groq client."""
#         try:
#             # Initialize embedding model (local)
#             self.embed_model = SentenceTransformer(self.embed_model_name)
#             logger.info(f"Loaded embedding model: {self.embed_model_name}")

#             # Initialize vector store (Chroma)
#             self.vector_store = chromadb.PersistentClient(path=self.vector_db_path)
#             self.collection = self.vector_store.get_or_create_collection(
#                 name="argo_metadata",
#                 metadata={"description": "ARGO float data metadata and summaries"}
#             )

#             # Initialize Groq client if API key available
#             if self.groq_key:
#                 self.groq_client = Groq(api_key=self.groq_key)
#                 logger.info(f"Groq client initialized with model: {self.groq_model}")

#             # Embed metadata if collection is empty
#             if self.collection and self.collection.count() == 0:
#                 self._embed_metadata()

#         except Exception as e:
#             logger.error(f"Error initializing LLM components: {e}")
#             logger.info("Falling back to deterministic responses")

#     def _build_knowledge_base(self) -> Dict[str, Any]:
#         """Build knowledge base for fallback responses."""
#         return {
#             "temperature_info": {
#                 "description": "Sea surface temperature measurements from ARGO floats",
#                 "range": "26-31°C in Indian Ocean surface waters",
#                 "patterns": "Seasonal variation with warmer temperatures in April-May"
#             },
#             "salinity_info": {
#                 "description": "Sea surface salinity measurements",
#                 "range": "34-36 PSU typical range",
#                 "patterns": "Generally stable with some seasonal variation"
#             },
#             "heat_content_info": {
#                 "description": "Ocean heat content representing thermal energy storage",
#                 "range": "5000-7000 typical values",
#                 "patterns": "Varies by location and season, higher values at 80°E"
#             },
#             "spatial_coverage": {
#                 "latitudes": "Equatorial region (0°)",
#                 "longitudes": "Indian Ocean 60°E to 100°E",
#                 "period": "2010-2013"
#             },
#             "data_availability": {
#                 "surface_timeseries": "High-frequency temperature and salinity",
#                 "monthly_averages": "Depth-resolved monthly climatology",
#                 "heat_content": "Integrated heat content time series"
#             }
#         }

#     def _embed_metadata(self):
#         """Create embeddings for data metadata and summaries."""
#         if not FULL_LLM_AVAILABLE or self.embed_model is None:
#             return
#         try:
#             metadata_docs = [
#                 "ARGO float surface temperature data from Indian Ocean covering 2010-2013 period",
#                 "Sea surface salinity measurements with seasonal variations",
#                 "Ocean heat content representing thermal energy in water column",
#                 "Vertical temperature and salinity profiles by depth",
#                 "Monthly climatological averages for oceanographic analysis",
#                 "Equatorial Indian Ocean data coverage from 60E to 100E longitude",
#                 "Temperature range 26-31 degrees Celsius in surface waters",
#                 "Salinity values typically 34-36 PSU practical salinity units",
#                 "Heat content variations between 5000-7000 energy units"
#             ]
#             embeddings = self.embed_model.encode(metadata_docs)
#             ids = [f"metadata_{i}" for i in range(len(metadata_docs))]
#             self.collection.add(
#                 embeddings=embeddings.tolist(),
#                 documents=metadata_docs,
#                 ids=ids,
#                 metadatas=[{"type": "data_summary", "index": i} for i in range(len(metadata_docs))]
#             )
#             logger.info(f"Embedded {len(metadata_docs)} metadata documents")
#         except Exception as e:
#             logger.error(f"Error embedding metadata: {e}")

#     def retrieve(self, query: str, n_results: int = 3) -> List[Dict[str, Any]]:
#         """Retrieve relevant documents using semantic similarity or keyword fallback."""
#         if not FULL_LLM_AVAILABLE or self.embed_model is None or self.collection is None:
#             return self._keyword_retrieve(query)
#         try:
#             query_embedding = self.embed_model.encode([query])
#             results = self.collection.query(
#                 query_embeddings=query_embedding.tolist(),
#                 n_results=n_results
#             )
#             retrieved_docs = []
#             for i, doc in enumerate(results['documents'][0]):
#                 retrieved_docs.append({
#                     "content": doc,
#                     "metadata": results['metadatas'][0][i],
#                     "similarity": results.get('distances', [[1.0]])[0][i]
#                 })
#             return retrieved_docs
#         except Exception as e:
#             logger.error(f"Error retrieving documents: {e}")
#             return self._keyword_retrieve(query)

#     def _keyword_retrieve(self, query: str) -> List[Dict[str, Any]]:
#         """Simple keyword-based retrieval fallback."""
#         query_lower = query.lower()
#         retrieved = []
#         if any(word in query_lower for word in ['temperature', 'temp', 'warm', 'cold']):
#             retrieved.append({
#                 "content": "Temperature data shows seasonal variation in Indian Ocean surface waters, ranging from 26-31°C",
#                 "metadata": {"type": "temperature_analysis"},
#                 "similarity": 0.8
#             })
#         if any(word in query_lower for word in ['salinity', 'salt']):
#             retrieved.append({
#                 "content": "Salinity measurements show values typically between 34-36 PSU with seasonal patterns",
#                 "metadata": {"type": "salinity_analysis"},
#                 "similarity": 0.8
#             })
#         if any(word in query_lower for word in ['heat content', 'thermal', 'energy']):
#             retrieved.append({
#                 "content": "Heat content represents thermal energy storage, varying by location with higher values at 80°E",
#                 "metadata": {"type": "heat_analysis"},
#                 "similarity": 0.8
#             })
#         if any(word in query_lower for word in ['location', 'where', 'longitude', 'latitude']):
#             retrieved.append({
#                 "content": "Data coverage spans equatorial Indian Ocean from 60°E to 100°E longitude during 2010-2013",
#                 "metadata": {"type": "spatial_info"},
#                 "similarity": 0.7
#             })
#         return retrieved[:3]

#     async def answer_with_context(self, query: str, retrieved_docs: List[Dict[str, Any]]) -> str:
#         """
#         Generate answer using retrieved context and Groq LLM.
#         """
#         if self.groq_client is None:
#             return self._generate_fallback_answer(query, retrieved_docs)
#         try:
#             context = "\n".join([doc["content"] for doc in retrieved_docs])
#             system_prompt = (
#                 "You are an expert oceanographer analyzing ARGO float data from the Indian Ocean. "
#                 "Use the provided context to answer questions about ocean temperature, salinity, heat content, "
#                 "and related oceanographic phenomena. Be specific and reference the data when possible. "
#                 "If the context doesn't contain enough information, say so clearly."
#             )
#             user_prompt = f"Context:\n{context}\n\nQuestion: {query}\n\nProvide a concise, data-grounded answer."

#             response = self.groq_client.chat.completions.create(
#                 model=self.groq_model,
#                 messages=[
#                     {"role": "system", "content": system_prompt},
#                     {"role": "user", "content": user_prompt}
#                 ],
#                 temperature=0.3,
#                 max_completion_tokens=500,
#             )
#             return response.choices[0].message.content.strip()
#         except Exception as e:
#             logger.error(f"Error generating LLM response: {e}")
#             return self._generate_fallback_answer(query, retrieved_docs)

#     def _generate_fallback_answer(self, query: str, retrieved_docs: List[Dict[str, Any]]) -> str:
#         """Generate deterministic answer without LLM."""
#         query_lower = query.lower()
#         if any(word in query_lower for word in ['temperature', 'temp', 'warm', 'cold']):
#             if '60' in query or '60e' in query_lower:
#                 return ("Based on the data, temperatures at 60°E longitude show seasonal variation. "
#                         "Surface temperatures typically range from 26-31°C, with warmer conditions "
#                         "during April-May period and cooler temperatures in winter months.")
#             elif '80' in query or '80e' in query_lower:
#                 return ("At 80°E longitude, sea surface temperatures follow similar seasonal patterns "
#                         "to 60°E, with typical ranges of 27-30°C. The data shows some year-to-year "
#                         "variability in the timing of maximum temperatures.")
#             else:
#                 return ("Temperature data from Indian Ocean ARGO floats shows seasonal variation "
#                         "with surface temperatures ranging from 26-31°C across the region.")
#         if any(word in query_lower for word in ['salinity', 'salt']):
#             return ("Salinity measurements from the ARGO floats show values typically between "
#                     "34-36 PSU (Practical Salinity Units). There is some seasonal variation "
#                     "and spatial differences across the Indian Ocean region.")
#         if any(word in query_lower for word in ['heat content', 'heat', 'energy']):
#             if 'compare' in query_lower or 'difference' in query_lower:
#                 return ("Heat content shows significant spatial variation across the Indian Ocean. "
#                         "Values at 80°E are generally higher (around 6000-6600 units) compared to "
#                         "60°E (around 5900-6300 units), indicating more thermal energy storage in the eastern region.")
#             else:
#                 return ("Ocean heat content represents the thermal energy stored in the water column. "
#                         "In this dataset, values typically range from 5000-7000 units, with seasonal "
#                         "and spatial variations across the Indian Ocean.")
#         if any(word in query_lower for word in ['trend', 'change', 'increase', 'decrease']):
#             return ("The 2010-2013 data shows seasonal patterns rather than clear long-term trends "
#                     "due to the relatively short time period. Longer time series would be needed "
#                     "to identify significant climate trends.")
#         if any(word in query_lower for word in ['where', 'location', 'longitude', 'latitude']):
#             return ("The dataset covers equatorial Indian Ocean locations primarily at 60°E and 80°E "
#                     "longitude, 0° latitude. Data spans the period from 2010 to 2013 with various "
#                     "measurement types including surface timeseries and depth profiles.")
#         if retrieved_docs:
#             context_summary = ". ".join([doc["content"][:100] + "..." for doc in retrieved_docs[:2]])
#             return f"Based on the available data: {context_summary}"
#         return ("Assistance is available for analyzing temperature, salinity, and heat content "
#                 "from Indian Ocean ARGO datasets spanning 2010–2013; please specify the aspect of interest.")

#     async def answer_query(self, query: str) -> str:
#         """Main entry point for answering user queries."""
#         try:
#             retrieved_docs = self.retrieve(query)
#             answer = await self.answer_with_context(query, retrieved_docs)
#             return answer
#         except Exception as e:
#             logger.error(f"Error processing query: {e}")
#             return ("An error occurred while processing the question; retry or adjust the query phrasing.")
            
# def natural_language_to_sql(query: str) -> Dict[str, Any]:
#     """
#     Example MCP-style function for mapping natural language to SQL queries.
#     """
#     query_lower = query.lower()
#     if 'temperature' in query_lower and 'average' in query_lower:
#         if '2012' in query:
#             return {
#                 "intent": "temperature_average",
#                 "sql": """
#                     SELECT AVG(temperature) as avg_temp, lat, lon
#                     FROM monthly_averages 
#                     WHERE EXTRACT(YEAR FROM time) = 2012 
#                       AND depth = 5.0
#                     GROUP BY lat, lon
#                 """,
#                 "parameters": {"year": 2012, "depth": 5.0},
#                 "description": "Average surface temperature by location for 2012"
#             }
#     if 'salinity' in query_lower and 'trend' in query_lower:
#         return {
#             "intent": "salinity_trend",
#             "sql": """
#                 SELECT time, temperature, salinity
#                 FROM surface_data 
#                 ORDER BY time
#             """,
#             "parameters": {},
#             "description": "Surface salinity time series for trend analysis"
#         }
#     if 'heat content' in query_lower and any(word in query_lower for word in ['compare', 'difference']):
#         return {
#             "intent": "heat_content_comparison",
#             "sql": """
#                 SELECT lon, AVG(heat_content) as avg_heat_content
#                 FROM heat_content
#                 WHERE lat = 0.0
#                 GROUP BY lon
#                 ORDER BY lon
#             """,
#             "parameters": {"lat": 0.0},
#             "description": "Heat content comparison across longitudes"
#         }
#     return {
#         "intent": "general_query",
#         "sql": "SELECT * FROM surface_data LIMIT 10",
#         "parameters": {},
#         "description": "General data sample"
#     }

# def test_natural_language_to_sql():
#     """Test cases for natural language to SQL mapping."""
#     test_queries = [
#         "What is the average temperature at 60°E in 2012?",
#         "Show me the salinity trends over time",
#         "How does heat content compare between different longitudes?",
#         "What are the typical measurements available?"
#     ]
#     expected_intents = [
#         "temperature_average",
#         "salinity_trend",
#         "heat_content_comparison",
#         "general_query"
#     ]
#     print("Testing Natural Language to SQL mapping:")
#     for i, query in enumerate(test_queries):
#         result = natural_language_to_sql(query)
#         print(f"\nQuery: {query}")
#         print(f"Intent: {result['intent']}")
#         print(f"SQL: {result['sql']}")
#         print(f"Expected: {expected_intents[i]} - {'✓' if result['intent'] == expected_intents[i] else '✗'}")

# if __name__ == "__main__":
#     test_natural_language_to_sql()



import os
import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import pandas as pd
from pathlib import Path

# Optional imports
try:
    from huggingface_hub import InferenceClient  # HF Inference API
    from sentence_transformers import SentenceTransformer
    import chromadb
    FULL_LLM_AVAILABLE = True
except ImportError:
    FULL_LLM_AVAILABLE = False
    logging.warning("LLM dependencies not fully available. Using fallback mode.")

from ..services.data_service import DataService
logger = logging.getLogger(__name__)

class LLMService:
    """
    Language model service for conversational data analysis.

    Implements RAG pipeline with vector similarity search and Hugging Face
    chat generation (Qwen2). Falls back to rule-based responses when HF API
    is not configured.
    """
    def __init__(self):
        self.data_service = DataService()
        # HF configuration
        self.hf_token = os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACEHUB_API_TOKEN")
        self.hf_model = os.getenv("HF_MODEL", "Qwen/Qwen2-7B-Instruct")
        self.embed_model_name = os.getenv("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
        self.vector_db_path = os.getenv("VECTOR_DB_PATH", "./vector_store")

        # Initialize components
        self.embed_model = None
        self.vector_store = None
        self.collection = None
        self.hf_client: Optional[InferenceClient] = None

        if FULL_LLM_AVAILABLE:
            self._initialize_llm_components()

        self.knowledge_base = self._build_knowledge_base()

    def _initialize_llm_components(self):
        """Initialize embedding model, vector store, and HF client."""
        try:
            # Embeddings (optional)
            try:
                self.embed_model = SentenceTransformer(self.embed_model_name)
                logger.info(f"Loaded embedding model: {self.embed_model_name}")
            except Exception as e:
                logger.warning(f"Embedding model unavailable: {e}")
                self.embed_model = None

            # Vector store (optional)
            try:
                self.vector_store = chromadb.PersistentClient(path=self.vector_db_path)
                self.collection = self.vector_store.get_or_create_collection(
                    name="argo_metadata",
                    metadata={"description": "ARGO float data metadata and summaries"}
                )
            except Exception as e:
                logger.warning(f"Chroma unavailable: {e}")
                self.vector_store = None
                self.collection = None

            # HF client
            if self.hf_token:
                # Using default provider (HF Inference API router)
                self.hf_client = InferenceClient(api_key=self.hf_token)
                logger.info(f"Hugging Face InferenceClient initialized with model: {self.hf_model}")
            else:
                logger.warning("HF_TOKEN not set; using deterministic fallback.")

            # Seed embeddings if vector store empty
            if self.collection and self.collection.count() == 0 and self.embed_model is not None:
                self._embed_metadata()

        except Exception as e:
            logger.error(f"Error initializing LLM components: {e}")
            logger.info("Falling back to deterministic responses")

    def _build_knowledge_base(self) -> Dict[str, Any]:
        return {
            "temperature_info": {"description": "Sea surface temperature measurements from ARGO floats",
                                 "range": "26-31°C in Indian Ocean surface waters",
                                 "patterns": "Seasonal variation with warmer temperatures in April-May"},
            "salinity_info": {"description": "Sea surface salinity measurements",
                              "range": "34-36 PSU typical range",
                              "patterns": "Generally stable with some seasonal variation"},
            "heat_content_info": {"description": "Ocean heat content representing thermal energy storage",
                                  "range": "5000-7000 typical values",
                                  "patterns": "Varies by location and season, higher values at 80°E"},
            "spatial_coverage": {"latitudes": "Equatorial region (0°)",
                                 "longitudes": "Indian Ocean 60°E to 100°E",
                                 "period": "2010-2013"},
            "data_availability": {"surface_timeseries": "High-frequency temperature and salinity",
                                  "monthly_averages": "Depth-resolved monthly climatology",
                                  "heat_content": "Integrated heat content time series"},
        }

    def _embed_metadata(self):
        if self.embed_model is None or self.collection is None:
            return
        try:
            docs = [
                "ARGO float surface temperature data from Indian Ocean covering 2010-2013 period",
                "Sea surface salinity measurements with seasonal variations",
                "Ocean heat content representing thermal energy in water column",
                "Vertical temperature and salinity profiles by depth",
                "Monthly climatological averages for oceanographic analysis",
                "Equatorial Indian Ocean data coverage from 60E to 100E longitude",
                "Temperature range 26-31 degrees Celsius in surface waters",
                "Salinity values typically 34-36 PSU practical salinity units",
                "Heat content variations between 5000-7000 energy units",
            ]
            embs = self.embed_model.encode(docs)
            self.collection.add(
                embeddings=embs.tolist(),
                documents=docs,
                ids=[f"metadata_{i}" for i in range(len(docs))],
                metadatas=[{"type": "data_summary", "index": i} for i in range(len(docs))],
            )
            logger.info(f"Embedded {len(docs)} metadata documents")
        except Exception as e:
            logger.error(f"Error embedding metadata: {e}")

    def retrieve(self, query: str, n_results: int = 3) -> List[Dict[str, Any]]:
        if self.embed_model is None or self.collection is None:
            return self._keyword_retrieve(query)
        try:
            qemb = self.embed_model.encode([query])
            res = self.collection.query(query_embeddings=qemb.tolist(), n_results=n_results)
            out = []
            for i, doc in enumerate(res['documents'][0]):
                out.append({
                    "content": doc,
                    "metadata": res['metadatas'][0][i],
                    "similarity": res.get('distances', [[1.0]])[0][i]
                })
            return out
        except Exception as e:
            logger.error(f"Error retrieving documents: {e}")
            return self._keyword_retrieve(query)

    def _keyword_retrieve(self, query: str) -> List[Dict[str, Any]]:
        q = query.lower()
        got = []
        if any(w in q for w in ['temperature', 'temp', 'warm', 'cold']):
            got.append({"content": "Temperature data shows seasonal variation in Indian Ocean surface waters, ranging from 26-31°C",
                        "metadata": {"type": "temperature_analysis"}, "similarity": 0.8})
        if any(w in q for w in ['salinity', 'salt']):
            got.append({"content": "Salinity measurements show values typically between 34-36 PSU with seasonal patterns",
                        "metadata": {"type": "salinity_analysis"}, "similarity": 0.8})
        if any(w in q for w in ['heat content', 'thermal', 'energy']):
            got.append({"content": "Heat content represents thermal energy storage, varying by location with higher values at 80°E",
                        "metadata": {"type": "heat_analysis"}, "similarity": 0.8})
        if any(w in q for w in ['location', 'where', 'longitude', 'latitude']):
            got.append({"content": "Data coverage spans equatorial Indian Ocean from 60°E to 100°E longitude during 2010-2013",
                        "metadata": {"type": "spatial_info"}, "similarity": 0.7})
        return got[:3]

    async def answer_with_context(self, query: str, retrieved_docs: List[Dict[str, Any]]) -> str:
        """Generate answer using retrieved context and HF Inference (Qwen2)."""
        if self.hf_client is None:
            return self._generate_fallback_answer(query, retrieved_docs)
        try:
            context = "\n".join([d["content"] for d in retrieved_docs])
            system_prompt = (
                "You are an expert oceanographer analyzing ARGO float data from the Indian Ocean. "
                "Use the provided context to answer questions about temperature, salinity, heat content, "
                "and related oceanographic phenomena. Be specific and reference the data when possible. "
                "If the context is insufficient, say so clearly."
            )
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}\n\nProvide a concise, data-grounded answer."}
            ]
            # OpenAI-compatible chat call on HF
            resp = self.hf_client.chat.completions.create(
                model=self.hf_model,
                messages=messages,
                temperature=0.3,
                max_tokens=500,
            )
            return resp.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error generating HF response: {e}")
            return self._generate_fallback_answer(query, retrieved_docs)

    def _generate_fallback_answer(self, query: str, retrieved_docs: List[Dict[str, Any]]) -> str:
        # unchanged fallback logic...
        q = query.lower()
        if any(w in q for w in ['temperature', 'temp', 'warm', 'cold']):
            if '60' in query or '60e' in q:
                return ("Based on the data, temperatures at 60°E longitude show seasonal variation. "
                        "Surface temperatures typically range from 26-31°C, with warmer conditions "
                        "during April-May period and cooler temperatures in winter months.")
            elif '80' in query or '80e' in q:
                return ("At 80°E longitude, sea surface temperatures follow similar seasonal patterns "
                        "to 60°E, with typical ranges of 27-30°C. The data shows some year-to-year "
                        "variability in the timing of maximum temperatures.")
            else:
                return ("Temperature data from Indian Ocean ARGO floats shows seasonal variation "
                        "with surface temperatures ranging from 26-31°C across the region.")
        if any(w in q for w in ['salinity', 'salt']):
            return ("Salinity measurements from the ARGO floats show values typically between "
                    "34-36 PSU (Practical Salinity Units). There is some seasonal variation "
                    "and spatial differences across the Indian Ocean region.")
        if any(w in q for w in ['heat content', 'heat', 'energy']):
            if 'compare' in q or 'difference' in q:
                return ("Heat content shows significant spatial variation across the Indian Ocean. "
                        "Values at 80°E are generally higher (around 6000-6600 units) compared to "
                        "60°E (around 5900-6300 units), indicating more thermal energy storage in the eastern region.")
            else:
                return ("Ocean heat content represents the thermal energy stored in the water column. "
                        "In this dataset, values typically range from 5000-7000 units, with seasonal "
                        "and spatial variations across the Indian Ocean.")
        if any(w in q for w in ['trend', 'change', 'increase', 'decrease']):
            return ("The 2010-2013 data shows seasonal patterns rather than clear long-term trends "
                    "due to the relatively short time period. Longer time series would be needed "
                    "to identify significant climate trends.")
        if any(w in q for w in ['where', 'location', 'longitude', 'latitude']):
            return ("The dataset covers equatorial Indian Ocean locations primarily at 60°E and 80°E "
                    "longitude, 0° latitude. Data spans the period from 2010 to 2013 with various "
                    "measurement types including surface timeseries and depth profiles.")
        if retrieved_docs:
            context_summary = ". ".join([d["content"][:100] + "..." for d in retrieved_docs[:2]])
            return f"Based on the available data: {context_summary}"
        return ("Assistance is available for analyzing temperature, salinity, and heat content "
                "from Indian Ocean ARGO datasets spanning 2010–2013; please specify the aspect of interest.")

    async def answer_query(self, query: str) -> str:
        try:
            retrieved_docs = self.retrieve(query)
            return await self.answer_with_context(query, retrieved_docs)
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return ("An error occurred while processing the question; retry or adjust the query phrasing.")

def natural_language_to_sql(query: str) -> Dict[str, Any]:
    # unchanged
    q = query.lower()
    if 'temperature' in q and 'average' in q and '2012' in query:
        return {"intent": "temperature_average", "sql": """
                SELECT AVG(temperature) as avg_temp, lat, lon
                FROM monthly_averages 
                WHERE EXTRACT(YEAR FROM time) = 2012 
                  AND depth = 5.0
                GROUP BY lat, lon
            """, "parameters": {"year": 2012, "depth": 5.0}, "description": "Average surface temperature by location for 2012"}
    if 'salinity' in q and 'trend' in q:
        return {"intent": "salinity_trend", "sql": """
                SELECT time, temperature, salinity
                FROM surface_data 
                ORDER BY time
            """, "parameters": {}, "description": "Surface salinity time series for trend analysis"}
    if 'heat content' in q and any(w in q for w in ['compare', 'difference']):
        return {"intent": "heat_content_comparison", "sql": """
                SELECT lon, AVG(heat_content) as avg_heat_content
                FROM heat_content
                WHERE lat = 0.0
                GROUP BY lon
                ORDER BY lon
            """, "parameters": {"lat": 0.0}, "description": "Heat content comparison across longitudes"}
    return {"intent": "general_query", "sql": "SELECT * FROM surface_data LIMIT 10", "parameters": {}, "description": "General data sample"}

def test_natural_language_to_sql():
    test_queries = [
        "What is the average temperature at 60°E in 2012?",
        "Show me the salinity trends over time",
        "How does heat content compare between different longitudes?",
        "What are the typical measurements available?"
    ]
    expected_intents = ["temperature_average", "salinity_trend", "heat_content_comparison", "general_query"]
    print("Testing Natural Language to SQL mapping:")
    for i, query in enumerate(test_queries):
        result = natural_language_to_sql(query)
        print(f"\nQuery: {query}")
        print(f"Intent: {result['intent']}")
        print(f"SQL: {result['sql']}")
        print(f"Expected: {expected_intents[i]} - {'✓' if result['intent'] == expected_intents[i] else '✗'}")

if __name__ == "__main__":
    test_natural_language_to_sql()