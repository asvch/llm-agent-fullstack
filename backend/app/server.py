from fastapi import FastAPI
from langserve import add_routes
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from agent import agent_with_chat_history

app = FastAPI(title="LLM Agent Romeo")

origins = [
    "http://localhost:8000",
    "http://localhost:8000/invoke"
    "http://localhost:3000",  # React frontend
    "https://asvch.github.io",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Input(BaseModel):
    input: str

class Output(BaseModel):
    output: str

add_routes(app, agent_with_chat_history, input_type=Input, output_type=Output)

@app.get("/")
def root():
    return {
        "message": "Server is running.",
    }

if __name__ == "__main__":
    import uvicorn

    # uvicorn.run(app, host="localhost", port=8000)  # to run server locally
    uvicorn.run(app, host="0.0.0.0", port=8000)