from pydantic import BaseModel, Field
from enum import Enum

class Status(str, Enum):
    incomplete='incomplete'
    completed='completed'

class CreateTaskModel(BaseModel):
    task: str = Field(..., min_length=1, max_length=25)

class DeleteTaskModel(BaseModel):
    task_id: str = Field(...)


