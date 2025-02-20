from bson import ObjectId
from pydantic import BaseModel, Field, validator
from typing import List

# Request schemas


class CreateTodoRequest(BaseModel):
    title: str
    description: str = ''
    status: str = 'Pending'
    tags: List[str] = []


class UpdateTodoRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str
    tags: List[str] | None = None

# Response schemas


class Todo(BaseModel):
    id: str = Field(default_factory=str, alias="_id")
    title: str
    description: str
    status: str
    tags: List[str] = []

    @validator("id", pre=True, always=True)
    def validate_id(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

    class Config:
        population_by_name = True
        json_encoders = {
            ObjectId: str
        }
