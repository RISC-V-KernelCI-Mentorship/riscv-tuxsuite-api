from typing import Literal, Optional, Union
from pydantic import BaseModel

class TuxSuiteTestStatus(BaseModel):
    tests: list[str]
    download_url: str
    uid: str
    device: str


class TuxSuiteBuildStatus(BaseModel):
    build_status: str
    download_url: str
    kernel_image_name: str
    target_arch: str
    toolchain: str
    modules: Union[str,  bool]
    uid: str
    kernel_version: str

class TuxSuiteTestRequest(BaseModel):
    kind: Literal['test']
    status: TuxSuiteTestStatus


class TuxSuiteBuildRequest(BaseModel):
    kind: Literal['kbuild', 'build']
    status: TuxSuiteBuildStatus