from fastapi import FastAPI, Body, Request
from db import insert_task, get_tasks, update_status, delete_task
from models import CreateTaskModel, Status
from mangum import Mangum
import jwt
from starlette.middleware.cors import CORSMiddleware


app = FastAPI()
handler = Mangum(app)
methods = [
    "OPTIONS",
    "GET",
    "POST",
    "PUT",
    "DELETE"
]

headers = [
    "Content-Type",
    "X-Amz-Date",
    "Authorization",
    "X-Api-Key",
    "X-Amz-Security-Token"
]

origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=methods,
    allow_headers=headers
)


def decode(token: str):
    return jwt.decode(token, algorithms=["RS256"], options={"verify_signature": False})


@app.post('/')
def create_task(request: Request, task_data: CreateTaskModel = Body(...)):
    token = request.headers.get("Authorization")
    task_id = insert_task(user_id=decode(token)["sub"], task=task_data.task)
    return {
        "message": "task created successfully",
        "task_id": task_id
        }


@app.get('/')
def read_task(request: Request):
    token = request.headers.get("Authorization")
    tasks_list = get_tasks(user_id=decode(token)["sub"])
    return {"tasks": tasks_list}


@app.put('/')
def update_task(request: Request, task_id: str, status: Status):
    token = request.headers.get("Authorization")
    if status.value == 'incomplete':
        status_updated = 'completed'
    else:
        status_updated = 'incomplete'

    update_status(task_id, status_updated, user_id=decode(token)["sub"])
    return {"message": "successfully!!!"}


@app.delete('/')
def remove_task(request: Request, task_id: str):
    token = request.headers.get("Authorization")
    delete_task(task_id, user_id=decode(token)["sub"])
    return {"message": "task deleted successfully!!!"}
