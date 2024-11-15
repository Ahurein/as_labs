from langchain_chroma import Chroma

from src.core.configs import Configs
from src.core.embedings import Embeddings


class Query:
    def __init__(self):
        self.CHROMA_PATH = 'chroma'
        self.DATA_PATH = 'data'
        self.db = Chroma(
            persist_directory=self.CHROMA_PATH, embedding_function=Embeddings.get_embedding()
        )
        self.embedding = Embeddings.get_embedding()

    def query(self, query: str):
        results = self.db.similarity_search_with_score(query, k=4,)
        print(results)