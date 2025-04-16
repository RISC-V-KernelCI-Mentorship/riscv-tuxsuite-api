from app.db import SessionDep
from app.db.tests import ScheduledTests
from fastapi import APIRouter
from app.schemas.request_schema import TuxSuiteTestSuite
from app.services.tuxsuite_service import run_tuxsuite_tests


router = APIRouter()

router.post("/run-tests", status_code=204)
def run_tests(tests_data: TuxSuiteTestSuite, session: SessionDep):
    test_uid = run_tuxsuite_tests(tests_data.kernel_image_url, tests_data.modules_url, tests_data.tests, "qemu-riscv64")
    scheduled_test = ScheduledTests(test_uid=test_uid, build_id=tests_data.build_id)
    session.add(scheduled_test)
    session.commit()
