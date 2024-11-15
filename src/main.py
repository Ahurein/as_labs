from fastapi import FastAPI

from src.core.db_load import DBLoad
from src.core.life_span import lifespan
from src.core.query import Query
from src.models.api_response import success_response

app = FastAPI(
    title= "AS labs",
    description= "Query PDF",
    version= "1.0",
    lifespan=lifespan
)


@app.get("/", tags=["Health"])
async def healthcheck():
    return success_response(message="Backend is running")