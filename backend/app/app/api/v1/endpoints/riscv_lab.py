from app.core.db import SessionDep
from app.models.tests import ScheduledTests
from fastapi import APIRouter
from app.schemas.tuxsuite import TuxSuiteTestSuite
from app.services.tuxsuite_service import run_tuxsuite_tests


router = APIRouter()

router.post("/run-tests", status_code=204)
def run_tests(tests_data: TuxSuiteTestSuite, session: SessionDep):
    """
    Schedules tests in tuxsuite.
    We only scheduledthe tests that have not been run for before for the build.
    """
    # TODO: should not run tests that have already been run
    test_uid = run_tuxsuite_tests(tests_data.kernel_image_url, tests_data.modules_url, tests_data.tests, "qemu-riscv64")
    scheduled_test = ScheduledTests(test_uid=test_uid, build_id=tests_data.build_id)
    session.add(scheduled_test)
    session.commit()
