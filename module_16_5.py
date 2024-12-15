from fastapi import FastAPI, Request, HTTPException, Body
from fastapi.responses import HTMLResponse, TemplateResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List

app = FastAPI()

templates = Jinja2Templates(directory="templates")

class User(BaseModel):
    id: int
    username: str
    age: int

users: List[User] = []

@app.get("/", response_class=TemplateResponse)
async def main(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})

@app.get("/user/{user_id}", response_class=TemplateResponse)
async def get_user(request: Request, user_id: int):
    user = next((user for user in users if user.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse("users.html", {"request": request, "user": user})

@app.post("/user/{username}/{age}", response_class=TemplateResponse)
async def create_user(request: Request, username: str, age: int):
    new_user = User(id=len(users) + 1, username=username, age=age)
    users.append(new_user)
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

@app.put("/user/{user_id}/{username}/{age}", response_class=TemplateResponse)
async def update_user(request: Request, user_id: int, username: str, age: int):
    user = next((user for user in users if user.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.username = username
    user.age = age
    return templates.TemplateResponse("users.html", {"request": request, "user": user})

@app.delete("/user/{user_id}", response_class=TemplateResponse)
async def delete_user(request: Request, user_id: int):
    user = next((user for user in users if user.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    users.remove(user)
    return templates.TemplateResponse("users.html", {"request": request, "users": users})
