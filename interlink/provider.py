from typing import List

from fastapi import HTTPException

from .spec import CreateStruct, LogRequest, Pod, PodRequest, PodStatus


class Provider:
    def create(self, pod: Pod) -> CreateStruct:
        raise HTTPException(status_code=500, detail="To be implemented by subclass")

    def delete(self, pod: PodRequest) -> None:
        raise HTTPException(status_code=500, detail="To be implemented by subclass")

    def status(self, pod: PodRequest) -> PodStatus:
        raise HTTPException(status_code=500, detail="To be implemented by subclass")

    def logs(self, req: LogRequest) -> bytes:
        raise HTTPException(status_code=500, detail="To be implemented by subclass")

    def create_pod(self, pod: Pod) -> CreateStruct:
        try:
            return self.create(pod)
        except Exception as ex:
            raise ex

    def delete_pod(self, pod: PodRequest) -> str:
        try:
            self.delete(pod)
        except Exception as ex:
            raise ex

        return f"Pod '{pod.metadata.uid}' deleted"

    def get_status(self, pods: List[PodRequest]) -> List[PodStatus]:
        return [self.status(pods[0])]

    def get_logs(self, req: LogRequest) -> bytes:
        try:
            return self.logs(req)
        except Exception as ex:
            raise ex
