from fastapi import FastAPI


app = FastAPI(
    title="TEST API",
    docs_url="/docs",
    version="0.0.1",
)
