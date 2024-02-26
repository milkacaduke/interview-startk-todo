
from fastapi import FastAPI, HTTPException, status
from fastapi.encoders import jsonable_encoder
from contextlib import asynccontextmanager
from myapp.database import init_db


from typing import List
from beanie import PydanticObjectId
from myapp.models.todo import Todo, UpdateTodo

from pprint import pprint

from myapp.config.config import get_config


# Handles on_startup, on_shutdown.
# Everything before yield will be run BEFORE the program start taking requests.
# Everthing after yield will be run AFTER program closes.
@asynccontextmanager
async def lifespan(app: FastAPI):

    config = get_config()
    pprint(config)

    # connect to db
    await init_db()
    yield

    

app = FastAPI(lifespan=lifespan)

@app.get("/", tags=["Root Check"])
async def index() -> dict:
    return {
        "message:": "Todo app root."
    }


@app.get("/todos", response_model=List[Todo], tags=["CRUD"])
async def get_todos():
    todos = await Todo.find_all().to_list()

    return todos


@app.post("/", status_code=status.HTTP_201_CREATED, response_model=Todo, tags=["CRUD"])
async def create_todo(todo: Todo):
    await todo.insert()

    return todo


@app.put("/todo/{id}", response_model=Todo, tags=["CRUD"])
async def update_todo(id: PydanticObjectId, todo_data: UpdateTodo):
    # Get todo by id
    todo = await Todo.get(id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo item not found. id: {id}"
        )

    # 
    json_compatible_item_data = jsonable_encoder(todo_data)
    dict_from_json_item_data = {k: v for k, v in json_compatible_item_data.items() if v is not None}
    
    _ = await todo.update({"$set": dict_from_json_item_data})
    updated_todo = await Todo.get(id)

    return updated_todo
    

@app.delete("/todo/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["CRUD"])
async def delete_todo(id: PydanticObjectId):
    # get todo by id
    todo = await Todo.get(id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, details=f"Todo item not found. id: {id}")
    
    # after we find it, we delete it.
    await todo.delete()

    return {"message": "Todo successfully deleted"}


@app.delete("/todos", status_code=status.HTTP_204_NO_CONTENT, tags=["Custom"])
async def delete_all():
    
    todos = await Todo.find_all().delete()

    return None
