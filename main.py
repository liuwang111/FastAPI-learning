from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="FastAPI Learning",
    version="0.1.0",
)


class UserCreate(BaseModel):
    name: str
    email: str
    age: int | None = None


@app.get("/")
def root():
    return {"message": "FastAPI is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/users/{user_id}")
def get_user(user_id: int, keyword: str | None = None):
    return {
        "user_id": user_id,
        "keyword": keyword,
    }


@app.post("/users")
def create_user(user: UserCreate):
    return {
        "message": "创建成功",
        "user": user,
    }