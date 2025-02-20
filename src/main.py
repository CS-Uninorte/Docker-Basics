from fastapi import FastAPI
from contextlib import asynccontextmanager
from bson import ObjectId
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware
from src.config import get_settings
from src.schemas.todos import (
    CreateTodoRequest,
    UpdateTodoRequest,
    Todo,
)
from typing import List


@asynccontextmanager
async def get_db(app: FastAPI):
    app.mongo_client = MongoClient(
        get_settings().DB_HOST, get_settings().DB_PORT)
    app.database = app.mongo_client.docker.todos
    yield
    app.mongo_client.close()

app = FastAPI(lifespan=get_db)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# routes


@app.get("/todos/get-all", response_model=List[Todo])
def get_todos():
    return app.database.find({"active": True}, {"active": 0})


@app.post("/todos/create")
def create_todo(todo: CreateTodoRequest):
    try:
        app.database.insert_one({
            **todo.model_dump(),
            "active": True
        })
    except Exception as e:
        print(f"The error is: {e}")
        return {"success": False, "message": "An error occurred while creating the todo"}

    return {"success": True, "message": "Todo created successfully"}


@app.put("/todos/update/{id}")
def update_todo(id: str, todo: UpdateTodoRequest):
    try:
        app.database.update_one(
            {"_id": ObjectId(id)},
            {"$set": todo.model_dump(exclude_unset=True)}
        )
    except Exception as e:
        print(f"The error is: {e}")
        return {"success": False, "message": "An error occurred while updating the todo"}

    return {"success": True, "message": "Todo updated successfully"}


@app.delete("/todos/delete/{id}")
def delete_todo(id: str):
    try:
        app.database.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"active": False}}
        )
    except Exception as e:
        print(f"The error is: {e}")
        return {"success": False, "message": "An error occurred while deleting the todo"}


    return {"success": True, "message": "Todo deleted successfully"}
