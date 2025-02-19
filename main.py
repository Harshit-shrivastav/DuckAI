import os
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from duckassist import DuckDuckAssist
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

load_dotenv()

app = FastAPI()
assist = DuckDuckAssist()

origins = [os.getenv("BASE_API_ORIGINS")]
ALLOWED_IPS = os.getenv("ALLOWED_IPS", "").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
"""
class IPWhitelistMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        client_ip = request.headers.get("X-Forwarded-For", request.client.host)
        client_ip = request.headers.get("CF-Connecting-IP", client_ip) 
        if client_ip not in ALLOWED_IPS:
            print("Blocked ip request: ",client_ip)
            raise HTTPException(status_code=403, detail="Access forbidden")
        return await call_next(request)

app.add_middleware(IPWhitelistMiddleware)
@app.middleware("http")
async def ip_whitelist_middleware(request: Request, call_next):
    forwarded_for = request.headers.get("X-Forwarded-For")
    client_ip = forwarded_for.split(",")[0].strip() if forwarded_for else request.client.host
    client_ip = request.headers.get("CF-Connecting-IP", client_ip)
    if client_ip not in ALLOWED_IPS:
        raise HTTPException(status_code=403, detail="Access forbidden")
    return await call_next(request)

class IPWhitelistMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        client_ip = request.headers.get("X-Forwarded-For", request.client.host)
        client_ip = request.headers.get("CF-Connecting-IP", client_ip) 
        if client_ip not in ALLOWED_IPS:
            print(f"Request blocked successfully from non-whitelisted IP: {client_ip}")
            return JSONResponse(
                content={"message": "Access denied. Your IP is not whitelisted."},
                status_code=403
            )
        return await call_next(request)
"""
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
    message: list = [{"role": "user", "content": ""}]
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
