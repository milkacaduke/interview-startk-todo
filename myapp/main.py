
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from myapp.database import init_db
from myapp.config.config import get_config

from typing import List
from beanie import PydanticObjectId

from myapp.routers import auth, todo

from myapp.models.todo_model import Todo, UpdateTodo, Comment
from myapp.models.user_model import User, UserIn, UserInDB
from myapp.dependency import get_current_user

from pprint import pprint


# Handles on_startup, on_shutdown.
# Everything before yield will be run BEFORE the program start taking requests.
# Everthing after yield will be run AFTER program closes.
@asynccontextmanager
async def lifespan(app: FastAPI):
    # connect to db
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(auth.router, tags=["Auth"], prefix="/auth")
app.include_router(todo.router, tags=["Todo"], prefix="/todo")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"])
async def index() -> dict:
    return {
        "message:": "Todo app root."
    }


""" Create """
@app.post("/", status_code=status.HTTP_201_CREATED, response_model=Todo, tags=["Todo"])
async def create_todo(todo: Todo):
    """ Create one todo """
    await todo.insert()
    return todo


""" Read """
@app.get("/todos", response_model=List[Todo], tags=["Todo"])
async def get_todos():
    """ Read all todo """
    todos = await Todo.find_all().to_list()
    return todos

@app.get("/todo/{id}", response_model=Todo, tags=["Todo"])
async def get_todo_by_id(id: str):
    todo = await Todo.get(id)
    if not todo:
        raise HTTPException (status_code = status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return todo


""" Update """
@app.put("/todo/{id}", response_model=Todo, tags=["Todo"])
async def update_todo(id: PydanticObjectId, todo_data: UpdateTodo):
    # Get todo by id
    todo = await Todo.get(id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo not found"
        )
    
    todo_dict = todo_data.model_dump(exclude_defaults=True)
    for k, v in todo_dict.items():
        setattr(todo, k, v)

    await todo.save()
    return todo

@app.put("/todo/{id}/comment", response_model=Todo, tags=["Todo"])
async def add_comment(id: PydanticObjectId, comment_data: Comment):
    todo = await Todo.get(id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo not found"
        )
    
    if not todo.comments:
        todo.comments = []

    todo.comments.append(comment_data)
    await todo.save()
    return todo

    
""" Delete """
@app.delete("/todo/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Todo"])
async def delete_todo(id: PydanticObjectId):
    todo = await Todo.get(id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo not found"
        )
    
    await todo.delete()
    return {"message": "Todo successfully deleted"}


@app.delete("/todos", status_code=status.HTTP_204_NO_CONTENT, tags=["Todo"])
async def delete_all():
    todos = await Todo.find_all().delete()
    return None


""" 
Auth Stuff


I need - 
    Endpoint:
        1. Register
        2. Login

    Auth / Token functions:
        1. create access token
        2. verify access token
        3. get current user - dependency injection

    Util functions:
        1. hash password 
            string -> hash
            hash -> string
    
            

Todo - 
    1. Create Utils file path
    2. Create User data model
    3. Create User register path
    4. Create User login path
    5. Retrive current user ( no auth )
    6. Retrive current user ( auth )

 """

@app.get("/users/me")
async def who_am_i(current_user: User = Depends(get_current_user)):
    return current_user
