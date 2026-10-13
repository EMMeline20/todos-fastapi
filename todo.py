from fastapi import APIRouter, Depends, HTTPException, Path, Request, status
from fastapi.templating import Jinja2Templates

from model import Todo

todo_router = APIRouter()
todo_list = []
templates = Jinja2Templates(directory="templates/")


@todo_router.post("/todo")
async def add_todo(request: Request, todo: Todo = Depends(Todo.as_form)):
    todo.id = len(todo_list) + 1
    todo_list.append(todo)
    return templates.TemplateResponse(request, "todo.html", {
        "todos": todo_list,
    })


@todo_router.get("/todo")
async def retrieve_todo(request: Request):
    return templates.TemplateResponse(request, "todo.html", {
        "todos": todo_list,
    })


@todo_router.get("/todo/{todo_id}")
async def get_single_todo(
    request: Request,
    todo_id: int = Path(..., title="The ID of the todo to retrieve."),
):
    for todo in todo_list:
        if todo.id == todo_id:
            return templates.TemplateResponse(request, "todo.html", {
                "todo": todo,
            })
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Todo with supplied ID doesn't exist",
    )