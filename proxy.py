import httpx
import os
import dotenv
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import Response

app = FastAPI()

HOST = os.getenv("BASE_API_HOST")
PORT = os.getenv("BASE_API_PORT")

BACKEND_URL = f"{HOST}:{PORT}"

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
async def reverse_proxy(path: str, request: Request):
    async with httpx.AsyncClient() as client:
        target_url = f"{BACKEND_URL}/{path}"
        headers = dict(request.headers)
        body = await request.body()

        response = await client.request(
            method=request.method, url=target_url, headers=headers, content=body
        )

        return Response(content=response.content, status_code=response.status_code, headers=dict(response.headers))

if __name__ == "__main__":
    uvicorn.run("proxy:app", host="0.0.0.0", port=80)
