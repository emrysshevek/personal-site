import subprocess
from typing import Annotated

from fastapi import FastAPI, Request, Header, Response
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "root"}


@app.post("/git-webhook")
async def git_webhook(x_github_event: Annotated[str, Header()], request: Request):
    response = {
        "message": "Ignored non-push event", 
        "event": x_github_event,
    }

    if x_github_event == "push":
        body = await request.json()
        response["branch"] = body["ref"]
        
        if body["ref"] == "refs/heads/production":
            instance = subprocess.run(["git", "pull"])
            if instance.returncode == 0:
                response["message"] = "success"
                return Response(content=response)
            else:
                response["message"] = str(instance.stderr)
                return Response(content=response, status_code=500)
        response["message"] = "Ignored non-production branch push"

    return Response(content=response)