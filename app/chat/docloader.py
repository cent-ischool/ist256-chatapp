import os

class FileCacheDocLoader:

    def __init__(self, file_cache):
        self._file_cache = file_cache

    def load_cached_document(self, key) -> str:
        filespec = os.path.join(self._file_cache, key) + ".md"
        with open(filespec, "r") as file:
            return file.read()
        
    def get_doc_list(self):
        return sorted([f.replace(".md","") for f in os.listdir(self._file_cache) if f.endswith(".md") and (f.find("LAB") != -1 or f.find("HW") != -1)])

if __name__=='__main__':
    folder = os.environ['LOCAL_FILE_CACHE']
    fcl = FileCacheDocLoader(folder)
    for key in fcl.get_doc_list():
        doc = fcl.load_cached_document(key)
        print(doc)
