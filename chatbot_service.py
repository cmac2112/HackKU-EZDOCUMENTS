import os
from pinecone import Pinecone
from llama_index.llms.gemini import Gemini
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core.storage.storage_context import StorageContext
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.core import ServiceContext, VectorStoreIndex, set_global_service_context
from llama_index.core import SummaryIndex, Document
from llama_index.core import Settings
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.retrievers import VectorIndexRetriever

class ChatbotService:
    def __init__(self, query, index):
        self.query = query
        self.index = index

    def input_query(self):
        PINECONE_API_KEY = 'a2f5dd3d-59f2-4a0a-99ed-0b6aa589247b'
        GOOGLE_API_KEY = 'AIzaSyAEWMjE0s5mlk3JjfYVo470EVLOf1OZioM'
        
        os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

        llm = Gemini(os.environ["GOOGLE_API_KEY"])
        embed_model = GeminiEmbedding(model_name="models/embedding-001")
        
        # Set the global service context
        service_context = ServiceContext.from_defaults(llm=llm, embed_model=embed_model)
        set_global_service_context(service_context)
        
        retriever = VectorIndexRetriever(index=self.index, similarity_top_k=10)
        query_engine = RetrieverQueryEngine(retriever=retriever)

        # Construct the query prompt
        engineered_prompt = ("You have been given text that comes from the user's school notes documents, "
                             "your job is to provide the user with an answer to their question and "
                             "provide context for where the answer came from in their notes. if you are unable to answer the question, "
                             "respond with your best guess or say that you are unable to answer the question."
                             "Make your response as detailed as possible to help the user understand the context of the answer. And format your response in a way that is easy to read. "
                             "also if possible, provide the user with a name to the document that contains the answer. "
                             "Here is the user query: ")
        
        together_prompt = engineered_prompt + self.query
        response = query_engine.query(together_prompt)
 
        return str(response)
    
    def generate_test(self):
        PINECONE_API_KEY = 'a2f5dd3d-59f2-4a0a-99ed-0b6aa589247b'
        GOOGLE_API_KEY = 'AIzaSyAEWMjE0s5mlk3JjfYVo470EVLOf1OZioM'
        
        os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

        llm = Gemini(os.environ["GOOGLE_API_KEY"])
        embed_model = GeminiEmbedding(model_name="models/embedding-001")
        
        # Set the global service context
        service_context = ServiceContext.from_defaults(llm=llm, embed_model=embed_model)
        set_global_service_context(service_context)
        
        retriever = VectorIndexRetriever(index=self.index, similarity_top_k=10)
        query_engine = RetrieverQueryEngine(retriever=retriever)

        # Construct the query prompt
        engineered_prompt = ("You have been given context that comes from the user's school notes,"
                             "your job here is to generate some test questions relevant to the topic given by the user,"
                             "and provide the user with the answers to the test questions at the very bottom,"
                             "Your format for generating the questions is to first provide the question, then provide choices for the user to choose from in a, b, c, d format,"
                             "and finally provide the correct answer to the question in the format of the correct choice in a, b, c, d format,"
                             "and make sure to make the questions nice and neat such that the the question is on top, and the choices are below the question,"
                             "Here is the user query: ")
        
        together_prompt = engineered_prompt + self.query
        response = query_engine.query(together_prompt)
 
        return str(response)