from fastapi import FastAPI

from app.core.db import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"Hello": "World"}
