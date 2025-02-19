import os
import asyncio
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from duckassist import DuckDuckAssist
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
assist = DuckDuckAssist()

# Load authorized IPs from environment variable
allowed_ips = [ip.strip() for ip in os.getenv("AUTHORIZED_IPS", "").split(",") if ip.strip()]

class IPWhitelistMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        if client_ip not in allowed_ips:
            return PlainTextResponse("request rejected", status_code=403)
        return await call_next(request)

# Add CORS middleware first
origins = [os.getenv("BASE_API_ORIGINS")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Add IP whitelist middleware after CORS
app.add_middleware(IPWhitelistMiddleware)

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
    message: list = [{"role": "user", "content": "Hey! Are you Alive?"}]
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
