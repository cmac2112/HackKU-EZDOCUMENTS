#have differnent functions depending on the type of interaction
#called upon by app.py
import chatbot_service
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

class InteractionHandler:
    def __init__(self, index):
        self.index = index
    def get_index(self):
        PINECONE_API_KEY = 'a2f5dd3d-59f2-4a0a-99ed-0b6aa589247b'
        pinecone_client = Pinecone(api_key=PINECONE_API_KEY)
        GOOGLE_API_KEY = 'AIzaSyAEWMjE0s5mlk3JjfYVo470EVLOf1OZioM'
        os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

        llm = Gemini(os.environ["GOOGLE_API_KEY"])
        #llama thinks we are using openai if i dont initialize this stuff here
        #even though no embedding is being done here
        embed_model = GeminiEmbedding(model_name="models/embedding-001")
        Settings.llm = llm
        Settings.embed_model = embed_model
        Settings.chunk_size = 512

        pinecone_index = pinecone_client.Index(self.index)
        vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
        #finding ther right vector storage in my account
        index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
        print(str(index))
        return index