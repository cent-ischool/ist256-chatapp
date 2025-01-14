from loguru import logger

from typing import List
from glob import glob
import os

import nbformat
from nbconvert import MarkdownExporter
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_core.documents import Document

class NotebookTransformer:
  
    def __init__(self, notebook_path: str, metadata :dict|None=None):
        with open(notebook_path) as fr:
            self._filename = notebook_path
            self._notebook = nbformat.reads(fr.read(), nbformat.NO_CONVERT)
            self._metadata = metadata

    def to_markdown(self, markdown_path: str|None=None):
        exporter = MarkdownExporter()
        self._markdown, resources = exporter.from_notebook_node(self._notebook)

        if markdown_path:
            with open(markdown_path, 'w') as fw:
                fw.write(self._markdown)
          
    def remove_empty_code_cells(self):    
        for cell in self._notebook.cells:
            if cell.cell_type == 'code' and cell.source.strip()=="":
                self._notebook.cells.remove(cell)
                logger.info(f"removed empty code cell filename={self._filename}")

    def remove_cells_after_markdown(self,markdown):
        total_cells = len(self._notebook.cells)
        for i in range(total_cells):
            cell = self._notebook.cells[i]
            if cell.cell_type == 'markdown' and cell.source.lower().strip().startswith(markdown.lower()):
                self._notebook.cells = self._notebook.cells[:i]
                logger.info(f"removed cells after markdown={markdown}, cells_removed={total_cells - i}")
                break

    def split(self) -> List[Document]:
        '''
        Break down into sections
        '''
        headers_to_split_on = [
            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3"),
        ]
        splitter=MarkdownHeaderTextSplitter(headers_to_split_on, return_each_line=False, strip_headers=False)    
        docs = splitter.split_text(self._markdown)
        logger.info(f"split notebook into count={len(docs)}, each with metadata={self._metadata}")
        for doc in docs:            
            doc.metadata = self._metadata
        return docs    

def extract_metadata(notebook_filename):
    doc_source = os.path.basename(notebook_filename)
    if doc_source.find("LAB") >=0:
        doc_type = "lab"
    elif doc_source.find("HW") >=0:
        doc_type = "homework"
    elif doc_source.find("Slides") >=0:
        doc_type = "slides"
    else:
        doc_type = "example"

    doc_unit_number = doc_source.split("-")[0]
    doc_unit_name = doc_source.split("_")[0].split("-")[1].lower()

    metadata = {
        "source": doc_source,
        "type": doc_type,
        "unit_number": doc_unit_number,
        "unit_name": doc_unit_name
    }
    logger.info(f"extracted metadata={metadata}")
    return metadata


if __name__ == '__main__':
  file_cache = os.environ['LOCAL_FILE_CACHE']
  globspec = os.path.join(file_cache, "*.ipynb")
  for notebookFile in glob(globspec):
    source = os.path.basename(notebookFile)
    metadata = extract_metadata(notebookFile)
    markdownFile = os.path.splitext(notebookFile)[0] + ".md"
    nbt = NotebookTransformer(notebookFile, metadata=metadata)
    nbt.remove_empty_code_cells()
    nbt.remove_cells_after_markdown("# Metacognition")
    nbt.remove_cells_after_markdown("## Part 3: Metacognition")
    nbt.to_markdown(markdownFile)
    docs = nbt.split()
    logger.info(f"converted notebook={notebookFile}, markdown={markdownFile}")


