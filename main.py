from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

import models
from database import engine
from routers import items, users
from core.config import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS設定（core/config.py の settings から取得）
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# カスタムエラーハンドリング（HTTPExceptionの統一フォーマット化）
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.status_code,
                "message": exc.detail,
            },
        },
    )


app.include_router(items.router)
app.include_router(users.router)


@app.get("/")
def read_root():
    return {"message": "Hello World"}