from typing import Annotated

from fastapi import FastAPI, Request, Header
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "root"}


@app.post("/git-webhook")
async def git_webhook(x_github_event: Annotated[str, Header()], request: Request):
    print(x_github_event)
    if x_github_event == "push":
        body = await request.json()
        if body["ref"] == "refs/heads/production":
            pass

    return {"event-type": x_github_event}