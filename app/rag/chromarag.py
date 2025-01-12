# import chromadb
# from chromadb.config import Settings
# from huggingface_hub import login

# from langchain_chroma import Chroma
# from langchain_huggingface import HuggingFaceEmbeddings

# class ChromaRAG:
#     def __init__(self, chroma_client, collection_name, embedding_function):
#         self.vectorstore = Chroma(
#             client=chroma_client,
#             collection_name=collection_name,
#             embedding_function=embedding_function
#         )

# if __name__=='__main__':
#     import os
#     hf_token =os.environ['HUGGINGFACE_TOKEN']
#     login(token=hf_token)
#     embeddings = HuggingFaceEmbeddings(model_name="hkunlp/instructor-base")
#     chroma_client = chromadb.HttpClient(
#         host=os.environ['CHROMADB_HOST'], 
#         port=os.environ['CHROMADB_PORT'],
#         settings=Settings(
#             chroma_client_auth_provider="chromadb.auth.token_authn.TokenAuthClientProvider",
#             chroma_client_auth_credentials=os.environ["CHROMA_CLIENT_AUTH_TOKEN"]
#         )    
#     ) 
#     chroma_client.heartbeat()
#     vectorstore = Chroma(
#         client=chroma_client,
#         collection_name="ist256",
#         embedding_function=embeddings
#     )