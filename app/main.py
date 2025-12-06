import uvicorn
from fastapi import (
    FastAPI,
    status,
)

from app.text_samples.root import RootPageTexts

app = FastAPI()


@app.get(
    path="/",
    status_code=status.HTTP_200_OK,
)
async def get_root() -> dict:
    return {
        "title": RootPageTexts.get_root_title(),
        "description": RootPageTexts.get_root_description(),
        "paths": {
            "swagger": "/docs",
            "redoc": "/redoc",
        },
    }


if __name__ == '__main__':
    uvicorn.run(
        'app.main:app',
        host="127.0.0.1",
        port=8081,
    )
