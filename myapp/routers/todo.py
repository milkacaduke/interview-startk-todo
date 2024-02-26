from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from beanie import PydanticObjectId
from myapp.models.todo_model import Todo, UpdateTodo, Comment
from myapp.dependency import get_current_user


router = APIRouter()


""" Create """
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Todo, tags=["Todo"])
async def create_todo(todo: Todo):
    """ Create one todo """
    await todo.insert()
    return todo


""" Read """
@router.get("/", response_model=List[Todo], tags=["Todo"])
async def get_todos():
    """ Read all todo """
    todos = await Todo.find_all().to_list()
    return todos

@router.get("/{id}", response_model=Todo, tags=["Todo"])
async def get_todo_by_id(id: str):
    todo = await Todo.get(id)
    if not todo:
        raise HTTPException (status_code = status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return todo


""" Update """
@router.put("/{id}", response_model=Todo, tags=["Todo"])
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

@router.put("/{id}/comment", response_model=Todo, tags=["Todo"])
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
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Todo"])
async def delete_todo(id: PydanticObjectId):
    todo = await Todo.get(id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo not found"
        )
    
    await todo.delete()
    return {"message": "Todo successfully deleted"}


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT, tags=["Todo"])
async def delete_all():
    todos = await Todo.find_all().delete()
    return None