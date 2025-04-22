
from typing import Literal, Optional
from pydantic import BaseModel


class TestResult(BaseModel):
    test_name: str
    test_collection: str
    result: Literal["FAIL", "ERROR", "MISS", "PASS", "DONE", "SKIP" ]
    logs: Optional[str] = None

class RunnerTestsResults(BaseModel):
    test_uid: str
    build_id: str
    tests: list[TestResult]
