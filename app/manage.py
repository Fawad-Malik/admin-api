from app import models, blueprints
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .settings import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(blueprints.router, tags=['Notes'], prefix='/api')


@app.get("/api/healthchecker")
def root():
    return {"message": "Welcome to Admin dashboard"}
