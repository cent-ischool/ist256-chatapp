# from loguru import logger

# import chromadb
# from chromadb.config import Settings
# from huggingface_hub import login

# from langchain_chroma import Chroma
# from langchain_huggingface import HuggingFaceEmbeddings

# class RAGAPI:
#     def __init__(
#             self,
#             huggingface_token: str,
#             huggingface_embedding_model: str,
#             chroma_host: str,
#             chroma_port: str,
#             chroma_auth_token: str,
#             collection_name: str
#         ):
#         login(token=huggingface_token)
#         self._embeddings = HuggingFaceEmbeddings(model_name=huggingface_embedding_model)
#         self._client = chromadb.HttpClient(
#             host=chroma_host,
#             port=chroma_port,
#             settings=Settings(
#                 chroma_client_auth_provider="chromadb.auth.token_authn.TokenAuthClientProvider",
#                 chroma_client_auth_credentials=chroma_auth_token
#             )    
#         ) 
#         self._client.heartbeat()
#         self._vectorstore = Chroma(
#             client=self._client,
#             collection_name=collection_name,
#             embedding_function=self._embeddings
#         )
#         logger.info(f"rag initialized chroma={chroma_host}:{chroma_port}, collection={collection_name}, embedding={huggingface_embedding_model}")

#     def search(
#             self, 
#             query: str, 
#             restrict_to_file: str|None = None, 
#             n_results: int = 5, 
#             threshold: float = 0.5
#         ):
#         if restrict_to_file:
#             filter = {"source": { "$eq": restrict_to_file }}
#             retriever = self._vectorstore.as_retriever(search_kwargs={"filter": filter})
#         else:
#             retriever = self._vectorstore.as_retriever()

#         results = retriever.vectorstore.similarity_search_with_relevance_scores(query, k=n_results, score_threshold=threshold)
#         logger.info(f"rag search returned count={len(results)}, min={min([score for doc, score in results])}, max={max([score for doc, score in results])}")
#         return results


#     def inject_prompt(
#             self, 
#             query: str,
#             rag_template: str, 
#             results: list
#         ):

#         if len(results) > 0:
#             documents = "\n\n".join([doc.page_content for doc, score in results])    
#             # add the documents to the prompt
#             final_prompt = rag_template.format(documents=documents, query=query)
#         else: # rag is no help
#             final_prompt = query # rag is no help
#         return final_prompt


# if __name__ == '__main__':
#     from time import sleep
#     import os
#     from constants import RAG_PROMPT_TEMPLATE
#     rag = RAGAPI(
#         huggingface_token=os.environ["HUGGINGFACE_TOKEN"],
#         huggingface_embedding_model="hkunlp/instructor-base",
#         chroma_host=os.environ['CHROMADB_HOST'],
#         chroma_port=os.environ['CHROMADB_PORT'],
#         chroma_auth_token=os.environ['CHROMA_CLIENT_AUTH_TOKEN'],
#         collection_name="ist256"
#     )
#     query = "What is the purpose of the for loop?"
#     docs = rag.search(query, n_results=3)
#     prompt = rag.inject_prompt(query, RAG_PROMPT_TEMPLATE, docs)
#     print(prompt)
#     sleep(2)
#     query = "What is the difference between a for and a while loop?"
#     docs = rag.search(query, n_results=3)
#     prompt = rag.inject_prompt(query, RAG_PROMPT_TEMPLATE, docs)
#     print(prompt)
