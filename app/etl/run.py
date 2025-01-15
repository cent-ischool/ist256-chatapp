import os
from loguru import logger
# from load import ChromaLoader
from extract import UrlContentExtractor
from transform import NotebookTransformer, extract_metadata

DOCUMENT_BASE = "https://raw.githubusercontent.com/ist256/spring2025/refs/heads/main/lessons/"
DOCUMENT_MANIFEST = [
    "01-Intro/LAB-Intro.ipynb",
    "02-Variables/LAB-Variables.ipynb",
    "02-Variables/HW-Variables.ipynb",
    "03-Conditionals/LAB-Conditionals.ipynb",
    "03-Conditionals/HW-Conditionals.ipynb",
    "04-Iterations/LAB-Iterations.ipynb",
    "04-Iterations/HW-Iterations.ipynb",
    "05-Functions/LAB-Functions.ipynb",
    "05-Functions/HW-Functions.ipynb",
    "06-Strings/LAB-Strings.ipynb",
    "06-Strings/HW-Strings.ipynb",
    "07-Files/LAB-Files.ipynb",
    "07-Files/HW-Files.ipynb",
    "08-Lists/LAB-Lists.ipynb",
    "08-Lists/HW-Lists.ipynb",
    "09-Dictionaries/LAB-Dictionaries.ipynb",
    "09-Dictionaries/HW-Dictionaries.ipynb",
    "10-Pandas-I/LAB-PandasI.ipynb",
    "10-Pandas-I/HW-PandasI.ipynb",
    "11-Pandas-II/LAB-PandasII.ipynb",
    "11-Pandas-II/HW-PandasII.ipynb",
    "12-Visualization/LAB-Visualization.ipynb",
    "12-Visualization/HW-Visualization.ipynb",
    "13-WebAPIs/LAB-Webapis.ipynb",
    "13-WebAPIs/HW-Webapis.ipynb",
    ]

def run_etl():
    from glob import glob
    # Setup
    extractor = UrlContentExtractor()
    # chroma_loader = ChromaLoader(
    #     huggingface_token=os.environ['HUGGINGFACE_TOKEN'],
    #     huggingface_embedding_model="hkunlp/instructor-base",
    #     chroma_host=os.environ['CHROMADB_HOST'],
    #     chroma_port=os.environ['CHROMADB_PORT'],
    #     chroma_auth_token=os.environ['CHROMA_CLIENT_AUTH_TOKEN'],
    #     collection_name="ist256"
    # )
    # chroma_loader.reset_collection()

    # Extract
    for doc in DOCUMENT_MANIFEST:
        extractor.extract_url(DOCUMENT_BASE, doc ,os.environ['LOCAL_FILE_CACHE'])
        logger.info(f"extracted={doc}, base={DOCUMENT_BASE}")

    # Transform
    for notebook in glob(os.path.join(os.environ['LOCAL_FILE_CACHE'], "*.ipynb")):
        markdownFile = os.path.splitext(notebook)[0] + ".md"
        transformer = NotebookTransformer(notebook, metadata=extract_metadata(notebook))
        transformer.remove_empty_code_cells()
        transformer.remove_cells_after_markdown("# Metacognition")
        transformer.remove_cells_after_markdown("## Part 3: Metacognition")
        transformer.to_markdown(markdownFile)

        # docs = transformer.split()
        # logger.info(f"transformed notebook={notebook}, docs={len(docs)}")

        # Load
        # chroma_loader.load(docs)
        # logger.info(f"loaded docs count={len(docs)}")

    # return loader for querying
    # return chroma_loader 

if __name__=='__main__':
    run_etl()


    # chroma_loader = ChromaLoader(
    #     huggingface_token=os.environ['HUGGINGFACE_TOKEN'],
    #     huggingface_embedding_model="hkunlp/instructor-base",
    #     chroma_host=os.environ['CHROMADB_HOST'],
    #     chroma_port=os.environ['CHROMADB_PORT'],
    #     chroma_auth_token=os.environ['CHROMA_CLIENT_AUTH_TOKEN'],
    #     collection_name="ist256"
    # )

    # query = "Can you help me complete the homework for iterations?"
    # results = chroma_loader.search(query, n_results=5)
    # #print(results)
    # for i in range(len(results["ids"][0])):
    #     print("((((("+ str(results["distances"][0][i]) + ")))))")
    #     print(results["metadatas"][0][i])
    #     print(results["documents"][0][i])
    #     print("\n")

