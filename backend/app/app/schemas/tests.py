
from typing import Literal, Optional
from app.core.runners import AVAILABLE_RUNNERS
from pydantic import BaseModel, Field


class TestResult(BaseModel):
    test_name: str = Field(description="Name of the test", examples=["ltp-smoke"])
    test_collection: str = Field(description="Name of the test collection", examples=["ltp"])
    result: Literal["FAIL", "ERROR", "MISS", "PASS", "DONE", "SKIP" ] = Field(description="Test result", examples=["PASS"])
    logs: Optional[str] = Field(default=None, description="Logs from the test run")

class RunnerTestsResults(BaseModel):
    test_uid: str = Field(description="Unique identifier from the runner", examples=["2wgX3BsGkUZMVs4JW6oMEoE2Qry"])
    build_id: str = Field(description="Build id inside KernelCI", examples=["maestro:681b69099ae9711e9ed49766"])
    tests: list[TestResult] = Field(description="List of test results")


class TestSuite(BaseModel):
    runner: AVAILABLE_RUNNERS = Field(default="tuxsuite", description="Runner that will run the tests")
    build_id: str = Field(description="Build id inside KernelCI", examples=["maestro:681b69099ae9711e9ed49766"])
    kernel_image_url: str = Field(description="Built kernel image URL", examples=["https://files.kernelci.org/kbuild-gcc-12-riscv-681b69099ae9711e9ed49766/Image"])
    modules_url: Optional[str] = Field(default=None, description="Built modules URL (must be compressed)", examples=["https://files.kernelci.org/kbuild-gcc-12-riscv-681b69099ae9711e9ed49766/modules.tar.xz"])
    tests: list[str] = Field(description="List of tests to run", examples=[["ltp-nptl", "ltp-fsx"]])
    collection: str = Field(description="Name of the tests collection", examples=["ltp"])
