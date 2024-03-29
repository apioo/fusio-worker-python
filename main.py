import sys

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

sys.path.append("./actions")
sys.path.append("./generated")

from worker import Worker, Execute, Update

app = FastAPI()
worker = Worker()


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"success": False, "message": str(exc)},
    )


@app.get("/")
def get():
    return worker.get()


@app.post("/{action}")
def execute(action: str, payload: Execute):
    return worker.execute(action, payload)


@app.put("/{action}")
def put(action: str, payload: Update):
    return worker.put(action, payload)


@app.delete("/{action}")
def put(action: str):
    return worker.delete(action)
