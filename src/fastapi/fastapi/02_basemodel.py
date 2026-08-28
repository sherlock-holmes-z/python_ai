import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    name: str = '无名氏'
    age: int = 18
    email: EmailStr | None = None

    def __str__(self) -> str:
        return f"{self.name} {self.age} {self.email}"


app = FastAPI()


@app.post("/user")
def get_user(user: User):
    # return str(user)
    return user.model_dump()  # 将user对象直接转json输出


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
