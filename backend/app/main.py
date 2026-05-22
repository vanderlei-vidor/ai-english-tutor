from fastapi import FastAPI
from app.routes.chat import router as chat_router
from app.routes.user import router as user_router

app = FastAPI()

app.include_router(chat_router)
app.include_router(user_router)


@app.get("/")
def root():
    return {"message": "English AI Backend Running"}
