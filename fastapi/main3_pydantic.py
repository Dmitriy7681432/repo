# -*- coding: utf-8 -*-
#https://github.com/artemonsh/fastapi-course/tree/4_database?tab=readme-ov-file
from fastapi import FastAPI
from pydantic import BaseModel,Field,EmailStr,ConfigDict

app = FastAPI()

data = {
    "email": "abc@email.ru",
    "bio": "Я пирожок",
    "age": 12,
}

data_wo_age = {
    "email": "abc@email.ru",
    "bio": "Я пирожок",
    # "gender": "male",
    # "birthday": "2022",
}

class UserSchema(BaseModel):
    email: EmailStr
    bio: str | None = Field(max_length=10)

    model_config = ConfigDict(extra='forbid')

users = []

@app.post("/users")
def add_user(user: UserSchema):
    users.append(user)
    return {"ok": True, "msg": "Юзер добавлен"}

@app.get("/users")
def get_users() -> list[UserSchema]:
    return users


# class UserAgeSchema(UserSchema):
#     age: int = Field(ge=0, le=130)


# print(repr(UserSchema(**data_wo_age)))
# print(repr(UserAgeSchema(**data)))