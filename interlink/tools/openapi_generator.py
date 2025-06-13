import json
import os.path
from pathlib import Path
from typing import List

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.responses import PlainTextResponse

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
import interlink as i

app = FastAPI()


@app.post("/create", summary="Create Pod", response_model_by_alias=True)
async def create_pod(pod: i.Pod) -> i.CreateStruct:
    raise NotImplementedError


@app.post("/delete", summary="Delete Pod")
async def delete_pod(pod: i.PodRequest) -> str:
    raise NotImplementedError


@app.get("/status", summary="Status Pod", response_model_by_alias=True)
async def get_status(pods: List[i.PodRequest]) -> List[i.PodStatus]:
    raise NotImplementedError


@app.get("/getLogs", summary="Get Logs", response_class=PlainTextResponse)
async def get_logs(req: i.LogRequest) -> PlainTextResponse:
    raise NotImplementedError


if __name__ == "__main__":
    root_path = Path(os.path.dirname(__file__)) / ".." / ".."
    openapi_schema_path = root_path / "docs" / "openapi" / "openapi.json"

    with open(root_path / "version.txt", encoding="utf-8") as fh:
        version = fh.read()

    with open(openapi_schema_path, "w", encoding="utf-8") as fh:
        json.dump(
            get_openapi(
                title="interLink Plugin spec",
                version=f"v{os.environ.get('VERSION', version)}",
                openapi_version=app.openapi()["openapi"],
                description="openapi spec for interLink apis <-> provider plugin communication",
                routes=app.routes,
            ),
            fh,
        )
