from langchain_community.document_loaders.pdf import PyPDFDirectoryLoader
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List

from src.core.embedings import Embeddings


class DBLoad:
    def __init__(self):
        self.CHROMA_PATH = 'chroma'
        self.DATA_PATH = 'data'

    def load_documents(self):
        loader = PyPDFDirectoryLoader(self.DATA_PATH)
        return loader.load()

    def split_docs_into_chunks(self, documents: List[Document]):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=80,
            length_function=len,
            is_separator_regex=False,
        )
        return splitter.split_documents(documents)

    def add_to_chroma(self, chunks: List[Document]):
        db = Chroma(
            persist_directory=self.CHROMA_PATH, embedding_function=Embeddings.get_embedding()
        )

        chunks_with_ids = self.calculate_chunk_ids(chunks)

        existing_items = db.get(include=[])
        existing_ids = set(existing_items["ids"])

        new_chunks = []
        for chunk in chunks_with_ids:
            if chunk.metadata["id"] not in existing_ids:
                new_chunks.append(chunk)
        if len(new_chunks):
            new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
            db.add_documents(new_chunks, ids=new_chunk_ids)

    def calculate_chunk_ids(self, chunks):
        last_page_id = None
        current_chunk_index = 0

        for chunk in chunks:
            source = chunk.metadata.get("source")
            page = chunk.metadata.get("page")
            current_page_id = f"{source}:{page}"

            if current_page_id == last_page_id:
                current_chunk_index += 1
            else:
                current_chunk_index = 0

            chunk_id = f"{current_page_id}:{current_chunk_index}"
            last_page_id = current_page_id

            chunk.metadata["id"] = chunk_id

        return chunks