import json
import os.path
from pathlib import Path
from typing import List

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.responses import PlainTextResponse

import interlink as i

app = FastAPI()


@app.post("/create", summary="Create pods", response_model_by_alias=True)
async def create_pod(pod: List[i.Pod]) -> i.CreateStruct:
    raise NotImplementedError


@app.post("/delete", summary="Delete pod")
async def delete_pod(pod: i.PodRequest) -> str:
    raise NotImplementedError


@app.get("/status", summary="Get Pods' status", response_model_by_alias=True)
async def get_status(pods: List[i.PodRequest]) -> List[i.PodStatus]:
    raise NotImplementedError


@app.get("/getLogs", summary="Get Pods' logs", response_class=PlainTextResponse)
async def get_logs(req: i.LogRequest) -> bytes:
    raise NotImplementedError


if __name__ == "__main__":
    root_path = Path(os.path.dirname(__file__)) / ".." / ".."
    openapi_schema_path = root_path / "docs" / "openapi" / "openapi.json"

    with open(root_path / "version.txt", encoding="utf-8") as fh:
        version = fh.read()

    with open(openapi_schema_path, "w", encoding="utf-8") as fh:
        json.dump(
            get_openapi(
                title="InterLink Plugin API",
                version=os.environ.get("VERSION", version),
                openapi_version=app.openapi()["openapi"],
                description="OpenAPI spec for InterLink API Server <-> Plugin communication",
                routes=app.routes,
            ),
            fh,
        )
