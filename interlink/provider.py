from typing import List

from fastapi import FastAPI, HTTPException

from .spec import CreateStruct, LogRequest, Pod, PodRequest, PodStatus


class Provider(FastAPI):
    def create(self, pod: Pod) -> CreateStruct:
        raise HTTPException(status_code=500, detail="NOT IMPLEMENTED YET")

    def delete(self, pod: PodRequest) -> None:
        raise HTTPException(status_code=500, detail="NOT IMPLEMENTED YET")

    def status(self, pod: PodRequest) -> PodStatus:
        raise HTTPException(status_code=500, detail="NOT IMPLEMENTED YET")

    def logs(self, req: LogRequest) -> bytes:
        raise HTTPException(status_code=500, detail="NOT IMPLEMENTED YET")

    def create_pod(self, pod: Pod) -> CreateStruct:
        try:
            self.create(pod)
        except Exception as ex:
            raise ex

        return "Containers created"

    def delete_pod(self, pod: PodRequest) -> str:
        try:
            self.delete(pod)
        except Exception as ex:
            raise ex

        return "Containers deleted"

    def get_status(self, pods: List[PodRequest]) -> List[PodStatus]:
        pod = pods[0]

        return [self.status(pod)]

    def get_logs(self, req: LogRequest) -> bytes:
        try:
            log_content = self.logs(req)
        except Exception as ex:
            raise ex

        return log_content
