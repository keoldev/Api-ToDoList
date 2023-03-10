from fastapi import FastAPI, Body, Request
from db import insert_task, get_tasks, update_status, delete_task
from models import CreateTaskModel, Status
from uuid import uuid4
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
    insert_task(user_id=decode(token)["sub"], task=task_data.task)
    return {"message": "task created successfully"}


@app.get('/')
def read_task(request: Request):
    token = 'eyJraWQiOiJyUFhVU3ZuOEhzYTRMWElBQ0VxYWk1ODJvZVZmRk9DbTczYUljSWdobHlJPSIsImFsZyI6IlJTMjU2In0.eyJhdF9oYXNoIjoiWGlhREl0d1hqbjFJMnJZWUVnTWtvQSIsInN1YiI6ImFmNWM2MTBmLWM1ZjQtNDE5ZC04MTE1LWI4NTczODdlYjc1MSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV9kZG9ZNnVLTmsiLCJjb2duaXRvOnVzZXJuYW1lIjoiYWY1YzYxMGYtYzVmNC00MTlkLTgxMTUtYjg1NzM4N2ViNzUxIiwiYXVkIjoiNmxxNzFraDczZmMwaTYxMTJ1NWYzOGdpM3QiLCJldmVudF9pZCI6ImNmYTczYmQ5LWYyOWEtNDk2Yy1hYTRkLWM1MTJjMGQ0YjJmNyIsInRva2VuX3VzZSI6ImlkIiwiYXV0aF90aW1lIjoxNjc4MzMyNzY3LCJleHAiOjE2NzgzMzYzNjcsImlhdCI6MTY3ODMzMjc2NywianRpIjoiNWM3ZjY0YTUtYTcwNC00YjJjLWEzOTktNjFiMDg5YjE0ZTdiIiwiZW1haWwiOiJrZXluZXJvbGl2b0BnbWFpbC5jb20ifQ.B5g3x8GIUPcFYQ3lMWSauYGiFouzkTNrrv6zMcpQEiL57Sgt-zklvxmKvmP9HYdUFFSi6uli3KFJrbuYMWbD0GYsm1vnpd4su4-Q-xAsfYLQwkaI59Yvgm0ATjFZeGfVxlfjhmRV0ISsJ8o9b3xiNqeDstbEdnZ0BF_yHQCjob3dHbH9LaSbdpOJ3IHEmHHcuqyVtBHLLVDAHmsj0AexCem2bsZbbtXERlLaIYKiZfgOiSrIW72Z3LT2NxW_SnbagYONakx6aLpglTA-dkVBu9ic-XpypWNI-yJeqtT4rKM9o2c2y3LAwJnQXQmeneXPGIzOIsQsvcrfZH7q93LPbQ'#request.headers.get("Authorization")
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
