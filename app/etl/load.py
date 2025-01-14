
from uuid import uuid4
from loguru import logger
from typing import List

import chromadb 
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from huggingface_hub import login

from langchain_core.documents import Document

class ChromaLoader:
    def __init__(
            self,
            huggingface_token: str,
            huggingface_embedding_model: str,
            chroma_host: str,
            chroma_port: str,
            chroma_auth_token: str,
            collection_name: str
        ):
        login(token=huggingface_token)
        self._collection_name = collection_name
        self._embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=huggingface_embedding_model)
        self._client = chromadb.HttpClient(
            host=chroma_host,
            port=chroma_port,
            settings=Settings(
                chroma_client_auth_provider="chromadb.auth.token_authn.TokenAuthClientProvider",
                chroma_client_auth_credentials=chroma_auth_token
            )    
        ) 
        self._client.heartbeat()
        logger.info(f"initialized chroma={chroma_host}:{chroma_port}, collection={collection_name}, embedding={huggingface_embedding_model}")

    def reset_collection(self):
        if self._collection_name in [ c.name for c in self._client.list_collections()]:
            self._client.delete_collection(name=self._collection_name)
            logger.info(f"reset collection={self._collection_name}")
        
        collection = self._client.create_collection(
            name=self._collection_name, 
            embedding_function=self._embedding_fn,     
            metadata={"hnsw:space": "cosine"}
        )

    def load(self, docs: List[Document]):
        collection = self._client.get_collection(name=self._collection_name, embedding_function=self._embedding_fn)
        ids = [ str(uuid4()) for _ in range(len(docs))]
        documents = [ d.page_content for d in docs]
        metadatas = [ d.metadata for d in docs]
        collection.add(ids=ids, documents=documents, metadatas=metadatas)
        
        logger.info(f"loaded docs count={collection.count()} into collection={self._collection_name}")
    

    def search(
            self, 
            query: str, 
            keyword: str|None = None, 
            n_results: int = 5, 
            threshold: float = 0.5
        ):
        ''' 
        Only exists for testing
        '''
        query_texts = [query]
        collection = self._client.get_collection(name=self._collection_name, embedding_function=self._embedding_fn)
        if keyword:
            docs = collection.query(query_texts=query_texts, n_results=n_results,where_document={"$contains": keyword})
        else:
            docs = collection.query(query_texts=query_texts, n_results=n_results)
        return docs
        
if __name__=='__main__':
    import os
    docs =[
        Document(page_content="this is a test of booger butts", metadata={"source": "test", "description": "booger document"}),
        Document(page_content="this is a test of bubble butts", metadata={"source": "test", "description": "bubble document"}),
        Document(page_content="this is a test of chickens", metadata={"source": "test", "description": "chicken document"}),

    ]
    chroma_loader = ChromaLoader(
        huggingface_token=os.environ["HUGGINGFACE_TOKEN"],
        huggingface_embedding_model="hkunlp/instructor-base",
        chroma_host=os.environ['CHROMADB_HOST'],
        chroma_port=os.environ['CHROMADB_PORT'],
        chroma_auth_token=os.environ['CHROMA_CLIENT_AUTH_TOKEN'],
        collection_name="test"
    )
    chroma_loader.reset_collection()
    chroma_loader.load(docs)
    results = chroma_loader.search("this is a test",keyword="booger", n_results=2)
    print(results)


