import uvicorn
from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.cors import CORSMiddleware
from model import Todo
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
from logging import getLogger
logger = getLogger(__name__)

from database import (
    fetch_one_todo,
    fetch_all_todos,
    create_todo,
    remove_todo,
    update_todo)

# app Object
app = FastAPI()

origins= ['https://localhost:3000']

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods =["*"],
#     allow_headers=["*"]
# )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Replace with your React app's origin
    allow_credentials=True,  # Set to True if cookies are required
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


@app.get("/")
def read_roots():
    return "Hello Kamlesh"


@app.get("/api/todo")
async def get_todo():
    response = await fetch_all_todos()
    return response

@app.get("/api/todo{title}", response_model=Todo)
async def get_todo_by_id(title):
    print(title)
    response = await fetch_one_todo(title)
    if response:
        return response
    raise HTTPException(404, f"there is no TODO item with this title {title}")


@app.post("/api/todo", response_model=Todo)
async def post_todo(todo: Todo):
    response = await create_todo(todo.dict())
    print("************************")
    if response:
        print(response)
        return todo
    raise HTTPException(400, "something went wrong/Bad request")

@app.put("/api/todo{title}", response_model=Todo)
async def put_todo(title:str, desc:str):
    print(title)
    response = await update_todo(title, desc)
    if response:
        return response
    raise HTTPException(404, f"there is no TODO item with this title {title}")

@app.delete("/api/todo/{title}")
async def delete_todo(title):
    logger.info("this is my first log")
    response = await remove_todo(title)
    if response:
        return "Successfully deleted todo Item"
    raise HTTPException(409, f"there is no TODO item with this title {title}")

if __name__ == "__main__":
    uvicorn.run(app, port=8000, host='127.0.0.1', reload=False)