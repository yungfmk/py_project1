from pydantic import BaseModel as bm
import uvicorn
from fastapi import FastAPI
from models import *

app = FastAPI()


class User(bm):
    username: str
    email: str
    age: int
    city: str


@app.post('/create_user/')
async def add_user(username: str = None, email: str = None, age: int = None, city: str = None):
    return create_user(username=username, email=email, age=age, city=city)


@app.delete('/delete_user/')
async def del_user(id_: int):
    return delete_user(id_)


@app.put('/update_user/')
async def upd_user(id_: int, username: str = None, email: str = None, age: int = None, city: str = None):
    return update_user(id_, username=username, email=email, age=age, city=city)


@app.post('/show_users/')
async def get_user(username: str = None):
    return show_users(username)


if __name__ == '__main__':
    uvicorn.run(app)
