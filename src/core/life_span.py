from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.core.db_load import DBLoad


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_load = DBLoad()
    docs = db_load.load_documents()
    chunks = db_load.split_docs_into_chunks(docs)
    db_load.add_to_chroma(chunks)
    yield