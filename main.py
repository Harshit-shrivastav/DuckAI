import os
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from duckassist import DuckDuckAssist
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
assist = DuckDuckAssist()

origins = [os.getenv("BASE_API_ORIGINS")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "API is Alive!"}


@app.get("/v1/get-token")
async def getToken():
    try:
        token = await asyncio.create_task(assist.getVQDToken())
        return {"message": "Success creating a token", "token": token}
    except:
        return HTTPException(500, "Error creating a token")


class ConversationBody(BaseModel):
    token: str = "use /v1/get-token to get token"
    model: str = "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo"
    message: list = [{"role": "user", "content": "Hey! Are you there ?"}]
    stream: bool = True


@app.post("/v1/chat/completions")
async def completions(body: ConversationBody):
    if body.stream:
        resp = StreamingResponse(
            assist.completionsStream(body.token, body.message, body.model),
            media_type="text/event-stream",
        )
    else:
        resp = StreamingResponse(
            assist.completions(body.token, body.message, body.model),
            media_type="text/plain",
        )
    return resp


if __name__ == "__main__":
    import uvicorn

    HOST = os.getenv("BASE_API_HOST")
    PORT = os.getenv("BASE_API_PORT")

    uvicorn.run("main:app", host=HOST, port=int(PORT), reload=True)
