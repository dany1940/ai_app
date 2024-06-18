from fastapi import FastAPI
from typing import Union



app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
# Dependency
