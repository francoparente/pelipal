from fastapi import FastAPI
from backend.src.routers import movies

app = FastAPI()
app.include_router(movies.router)

@app.get("/")
def read_root():
    return {"message": "Pelipal API funcionando"}

