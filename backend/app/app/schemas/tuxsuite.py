from typing import Literal, Union
from pydantic import BaseModel, Field

class TuxSuiteTestStatus(BaseModel):
    """
    More details can be found in TuxSuite documentation: https://docs.tuxsuite.com/callbacks/
    """
    tests: list[str] = Field(description="Tests that were run", examples=[["ltp-smoke"]])
    download_url: str = Field(description="URL where tests results can be downloaded from", examples=["https://storage.tuxsuite.com/public/tuxsuite/demo/tests/2MBYa8FhoBHkRCX2BMMPusjuClf/"])
    uid: str = Field(description="Unique identifier of this test run", examples=["2MBYa8FhoBHkRCX2BMMPusjuClf"])
    device: str = Field(description="Device where tests were run", examples=["qemu-riscv64"])


class TuxSuiteBuildStatus(BaseModel):
    """
    More details can be found in TuxSuite documentation: https://docs.tuxsuite.com/callbacks/
    """
    build_status: str = Field(description="Status result of the build", examples=["pass"])
    download_url: str = Field(description="URL where build results can be downloaded from", examples=["https://storage.tuxsuite.com/public/tuxsuite/demo/tests/2MBYa8FhoBHkRCX2BMMPusjuClf/"])
    kernel_image_name: str = Field(description="Kernel image name", examples=["Image.gz"])
    target_arch: str = Field(description="Target arch for the build", examples=["riscv"])
    toolchain: str = Field(description="Used toolchain", examples=["gcc-12"])
    modules: Union[str,  bool] = Field(description="Resulting modules", examples=[False, "modules.xz"])
    uid: str = Field(description="Unique identifier of this build", examples=["2MBYa8FhoBHkRCX2BMMPusjuClf"])
    kernel_version: str = Field(description="Version of the kernel", examples=["6.7.0-rc4"])

class TuxSuiteTestRequest(BaseModel):
    kind: Literal['test'] = Field(description="Type of the callback")
    status: TuxSuiteTestStatus = Field(description="Status of the test")


class TuxSuiteBuildRequest(BaseModel):
    kind: Literal['kbuild', 'build'] = Field(description="Type of callback")
    status: TuxSuiteBuildStatus = Field(description="Status of the build")