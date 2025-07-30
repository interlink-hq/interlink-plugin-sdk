import datetime
from typing import Annotated, Dict, List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

# Note: Some models below are extensions to the core v0.5.0 OpenAPI spec
# for backward compatibility and extended functionality


class Metadata(BaseModel):
    name: Optional[str] = None
    namespace: Optional[str] = None
    uid: Optional[str] = None
    annotations: Optional[Dict[str, str]] = Field({})
    labels: Optional[Dict[str, str]] = Field({})
    generate_name: Annotated[str | None, Field(alias="generateName")] = None
    model_config = ConfigDict(populate_by_name=True)


class VolumeMount(BaseModel):
    name: str
    mount_path: Annotated[str, Field(alias="mountPath")]
    sub_path: Annotated[str | None, Field(alias="subPath")] = None
    read_only: Annotated[bool | None, Field(alias="readOnly")] = False
    mount_propagation: Annotated[str | None, Field(alias="mountPropagation")] = None
    model_config = ConfigDict(populate_by_name=True)


class ConfigMapKeySelector(BaseModel):
    key: str
    name: Optional[str] = None
    optional: Optional[bool] = None


class SecretKeySelector(BaseModel):
    key: str
    name: Optional[str] = None
    optional: Optional[bool] = None


class EnvVarSource(BaseModel):
    config_map_key_ref: Annotated[
        ConfigMapKeySelector | None, Field(alias="configMapKeyRef")
    ] = None
    secret_key_ref: Annotated[SecretKeySelector | None, Field(alias="secretKeyRef")] = (
        None
    )
    model_config = ConfigDict(populate_by_name=True)


class EnvVar(BaseModel):
    name: str
    value: Optional[str] = None
    value_from: Annotated[EnvVarSource | None, Field(alias="valueFrom")] = None
    model_config = ConfigDict(populate_by_name=True)


class SecurityContext(BaseModel):
    allow_privilege_escalation: Annotated[
        bool | None, Field(alias="allowPrivilegeEscalation")
    ] = None
    privileged: Optional[bool] = None
    proc_mount: Annotated[str | None, Field(alias="procMount")] = None
    read_only_file_system: Annotated[bool | None, Field(alias="readOnlyFileSystem")] = (
        None
    )
    run_as_group: Annotated[int | None, Field(alias="runAsGroup")] = None
    run_as_non_root: Annotated[bool | None, Field(alias="runAsNonRoot")] = None
    run_as_user: Annotated[int | None, Field(alias="runAsUser")] = None
    model_config = ConfigDict(populate_by_name=True)


class ContainerPort(BaseModel):
    container_port: Annotated[int, Field(alias="containerPort")]
    host_ip: Annotated[str | None, Field(alias="hostIp")] = None
    host_port: Annotated[int | None, Field(alias="hostPort")] = None
    name: Optional[str] = None
    protocol: Optional[str] = None
    model_config = ConfigDict(populate_by_name=True)


class Container(BaseModel):
    name: str
    image: str
    tag: str = "latest"
    command: Optional[List[str]] = None
    args: Optional[List[str]] = Field([])
    resources: Optional[dict] = Field({})
    volume_mounts: Annotated[List[VolumeMount] | None, Field(alias="volumeMounts")] = []
    env: Optional[List[EnvVar]] = None
    security_context: Annotated[
        SecurityContext | None, Field(alias="securityContext")
    ] = None
    ports: Optional[List[ContainerPort]] = None  # Extension: not in v0.5.0 core spec
    model_config = ConfigDict(populate_by_name=True)


class KeyToPath(BaseModel):
    key: Optional[str]
    path: str
    mode: Optional[int] = None


class SecretVolumeSource(BaseModel):
    secret_name: Annotated[str, Field(alias="secretName")]
    items: Optional[List[KeyToPath]] = Field([])
    optional: Optional[bool] = None
    default_mode: Annotated[int | None, Field(alias="defaultMode")] = None
    model_config = ConfigDict(populate_by_name=True)


class ConfigMapVolumeSource(BaseModel):
    name: str
    items: Optional[List[KeyToPath]] = Field([])
    optional: Optional[bool] = None
    default_mode: Annotated[int | None, Field(alias="defaultMode")] = None
    model_config = ConfigDict(populate_by_name=True)


class PersistentVolumeClaimVolumeSource(BaseModel):
    claim_name: Annotated[str, Field(alias="claimName")]
    read_only: Annotated[bool | None, Field(alias="readOnly")] = None
    model_config = ConfigDict(populate_by_name=True)


class PodVolume(BaseModel):
    name: str
    empty_dir: Annotated[dict | None, Field(alias="emptyDir")] = None
    secret: Optional[SecretVolumeSource] = None
    config_map: Annotated[ConfigMapVolumeSource | None, Field(alias="configMap")] = None
    persistent_volume_claim: Annotated[
        PersistentVolumeClaimVolumeSource | None, Field(alias="persistentVolumeClaim")
    ] = None
    model_config = ConfigDict(populate_by_name=True)


class PodSpec(BaseModel):
    containers: List[Container]
    init_containers: Annotated[List[Container] | None, Field(alias="initContainers")] = (
        None
    )
    volumes: Optional[List[PodVolume]] = None
    preemption_policy: Annotated[str | None, Field(alias="preemptionPolicy")] = None
    priority_class_name: Annotated[str | None, Field(alias="priorityClassName")] = None
    priority: Optional[int] = None
    restart_policy: Annotated[str | None, Field(alias="restartPolicy")] = None
    termination_grace_period_seconds: Annotated[
        int | None, Field(alias="terminationGracePeriodSeconds")
    ] = None
    model_config = ConfigDict(populate_by_name=True)


class PodRequest(BaseModel):
    metadata: Metadata
    spec: PodSpec


class ConfigMap(BaseModel):
    metadata: Metadata
    data: Optional[dict]
    binary_data: Annotated[dict | None, Field(alias="binaryData")] = None
    type: Optional[str] = None
    immutable: Optional[bool] = None
    model_config = ConfigDict(populate_by_name=True)


class Secret(BaseModel):
    metadata: Metadata
    data: Optional[dict] = None
    string_data: Annotated[dict | None, Field(alias="stringData")] = None
    type: Optional[str] = None
    immutable: Optional[bool] = None
    model_config = ConfigDict(populate_by_name=True)


class VolumeResourceRequirements(BaseModel):
    requests: dict[str, str]  # e.g.: {"storage": "1Gi"}
    limits: Optional[dict[str, str]] = None


class LabelSelectorRequirement(BaseModel):
    key: str
    operator: str
    values: Optional[List[str]] = None


class LabelSelector(BaseModel):
    match_labels: Annotated[Optional[dict[str, str]], Field(alias="matchLabels")] = None
    match_expressions: Annotated[
        Optional[List[LabelSelectorRequirement]], Field(alias="matchExpressions")
    ] = None
    model_config = ConfigDict(populate_by_name=True)


class TypedLocalObjectReference(BaseModel):
    api_group: Annotated[Optional[str], Field(alias="apiGroup")] = None
    kind: str
    name: str
    model_config = ConfigDict(populate_by_name=True)


class TypedObjectReference(BaseModel):
    api_group: Annotated[Optional[str], Field(alias="apiGroup")] = None
    kind: str
    name: str
    namespace: Optional[str] = None
    model_config = ConfigDict(populate_by_name=True)


class PersistentVolumeClaimSpec(BaseModel):
    access_modes: Annotated[
        List[Literal["ReadWriteOnce", "ReadOnlyMany", "ReadWriteMany"]],
        Field(alias="accessModes"),
    ]
    data_source: Annotated[
        TypedLocalObjectReference | None, Field(alias="dataSource")
    ] = None
    data_source_ref: Annotated[
        TypedObjectReference | None, Field(alias="dataSourceRef")
    ] = None
    resources: VolumeResourceRequirements
    selector: Optional[LabelSelector] = None
    storage_class_name: Annotated[Optional[str], Field(alias="storageClassName")] = None
    volume_attributes_class_name: Annotated[
        Optional[str], Field(alias="volumeAttributesClassName")
    ] = None
    volume_mode: Annotated[Optional[str], Field(alias="volumeMode")] = None
    volume_name: Annotated[Optional[str], Field(alias="volumeName")] = None
    model_config = ConfigDict(populate_by_name=True)


class PersistentVolumeClaim(BaseModel):
    metadata: Metadata
    spec: PersistentVolumeClaimSpec


class Volume(BaseModel):
    name: str
    config_maps: Annotated[List[ConfigMap] | None, Field(alias="configMaps")] = None
    secrets: Optional[List[Secret]] = None
    empty_dirs: Annotated[List[str] | None, Field(alias="emptyDirs")] = None
    persistent_volume_claims: Annotated[
        List[PersistentVolumeClaim] | None, Field(alias="persistentVolumeClaims")
    ] = None
    model_config = ConfigDict(populate_by_name=True)


class Pod(BaseModel):
    pod: PodRequest
    container: List[Volume]


class StateTerminated(BaseModel):
    exit_code: Annotated[int, Field(alias="exitCode")]
    reason: Optional[str] = None
    model_config = ConfigDict(populate_by_name=True)


class StateRunning(BaseModel):
    started_at: Annotated[str | None, Field(alias="startedAt")] = None
    model_config = ConfigDict(populate_by_name=True)


class StateWaiting(BaseModel):
    message: Optional[str] = None
    reason: Optional[str] = None


class ContainerStates(BaseModel):
    terminated: Optional[StateTerminated] = None
    running: Optional[StateRunning] = None
    waiting: Optional[StateWaiting] = None


class ContainerStatus(BaseModel):
    name: str
    state: ContainerStates


class PodStatus(BaseModel):
    name: str
    uid: Annotated[str, Field(alias="UID")]
    jid: Annotated[str | None, Field(alias="JID")] = None
    namespace: str
    containers: List[ContainerStatus]
    model_config = ConfigDict(populate_by_name=True)


class LogOpts(BaseModel):
    tail: Annotated[int | None, Field(alias="Tail")] = None
    limit_bytes: Annotated[int | None, Field(alias="LimitBytes")] = None
    timestamps: Annotated[bool | None, Field(alias="Timestamps")] = None
    previous: Annotated[bool | None, Field(alias="Previous")]
    since_seconds: Annotated[int | None, Field(alias="SinceSeconds")] = None
    since_time: Annotated[datetime.datetime | None, Field(alias="SinceTime")] = None
    model_config = ConfigDict(populate_by_name=True)


class LogRequest(BaseModel):
    namespace: Annotated[str, Field(alias="Namespace")]
    pod_uid: Annotated[str, Field(alias="PodUID")]
    pod_name: Annotated[str, Field(alias="PodName")]
    container_name: Annotated[str, Field(alias="ContainerName")]
    opts: Annotated[LogOpts, Field(alias="Opts")]
    model_config = ConfigDict(populate_by_name=True)


class CreateStruct(BaseModel):
    pod_uid: Annotated[str, Field(alias="PodUID")]
    pod_jid: Annotated[str, Field(alias="PodJID")]
    model_config = ConfigDict(populate_by_name=True)
