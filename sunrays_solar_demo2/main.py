import uvicorn as uvicorn
from fastapi import FastAPI
import os

from routes.user_router import router as user_route
from routes.category_router import category as category_route

app = FastAPI()
app.include_router(user_route, prefix='/user')
app.include_router(category_route, prefix='/category')


if __name__ == "__main__":
    server_port: int = int(os.environ.get("PORT", 8000))
    server_host: str = os.environ.get("HOST", "localhost")
    uvicorn.run("main:app", port=server_port, host=server_host)
