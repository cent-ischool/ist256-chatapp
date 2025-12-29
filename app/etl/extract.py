from loguru import logger

import requests
import os 



class UrlContentExtractor:
    def __init__(self):
        pass

    def extract_url(self, base, filename, destination_folder):
        url = f"{base}{filename}"
        response = requests.get(url)
        response.raise_for_status()
        folder, file = filename.split('/')
        clean_filename = folder.split('-')[0] + '-' + file
        localfile = os.path.join(destination_folder, clean_filename)
        with open(localfile, 'w') as f:
            f.write(response.text)


if __name__=='__main__':
    DOCUMENT_BASE = "https://raw.githubusercontent.com/ist256/spring2025/refs/heads/main/lessons/"
    DOCUMENT_MANIFEST = [
        "04-Iterations/Slides.ipynb",
        "04-Iterations/LAB-Iterations.ipynb",
        "04-Iterations/HW-Iterations.ipynb",
        "05-Functions/LAB-Functions.ipynb",
        "05-Functions/HW-Functions.ipynb",]
    extractor = UrlContentExtractor()
    for doc in DOCUMENT_MANIFEST:
        extractor.extract_url(DOCUMENT_BASE, doc ,os.environ['LOCAL_FILE_CACHE'].replace('"',''))
        logger.info(f"extracted={doc}, base={DOCUMENT_BASE}")
