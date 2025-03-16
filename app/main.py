from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from app.schema import HTMLData
from app.utils import process_video

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/parse_html")
async def parse_html(data: HTMLData):
    try:
        process_video(data)
        return {"status": "success", "message": "Видео загружено успешно"}

    except Exception as e:
        logger.exception("Внутренняя ошибка сервера")
        raise HTTPException(
            status_code=500, detail=f"Внутренняя ошибка сервера: {str(e)}"
        )
