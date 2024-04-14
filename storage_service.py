import os
from pinecone import Pinecone
from llama_index.llms.gemini import Gemini
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core.storage.storage_context import StorageContext
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.core import ServiceContext, VectorStoreIndex, set_global_service_context
from llama_index.core import SummaryIndex, Document


class StorageService:
    def __init__(self, texts):
        self.texts = texts
        #texts is a list of strings that are the paragraphs of the documents

    def get_embed_and_store(self):
        GOOGLE_API_KEY = 'AIzaSyAEWMjE0s5mlk3JjfYVo470EVLOf1OZioM'
        PINECONE_API_KEY = 'a2f5dd3d-59f2-4a0a-99ed-0b6aa589247b' #dont steal pls

        os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
        os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
        llm = Gemini(os.environ["GOOGLE_API_KEY"])

        # Create a Pinecone vector store
        pinecone_client = Pinecone(api_key=os.environ["PINECONE_API_KEY"])

        ind = SummaryIndex([])
        doc_chunks = []
        #begin adding documents to the index
        for i, text in enumerate(self.texts):
            doc = Document(text=text, id_=f'doc_id_{i}')
            doc_chunks.append(doc)
        
        for doc_chunk in doc_chunks:
            ind.insert(doc_chunk)
        
        pinecone_index = pinecone_client.Index("hackku")
        #embed the documents and store them in the index
        gemini_embed_model = GeminiEmbedding(model_name="models/embedding-001")
        service_context = ServiceContext.from_defaults(llm=llm, embed_model=gemini_embed_model)
        set_global_service_context(service_context)
        
        storage_context = StorageContext.from_defaults(vector_store=PineconeVectorStore(pinecone_index=pinecone_index))
        
        index = VectorStoreIndex.from_documents(doc_chunks, storage_context=storage_context)

        print("storage done")

    #extra function to store the document names to be used by flask to display document names
    #on the notes page
    def store_doc_names(self, texts):
        doc_names = []
        for i in texts:
            doc_names.append(i)
