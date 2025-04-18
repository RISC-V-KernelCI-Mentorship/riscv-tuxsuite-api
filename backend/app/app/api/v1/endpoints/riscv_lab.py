from app.core.db import SessionDep
from app.models.tests import ScheduledTest, RunTest
from app.schemas.tuxsuite import TuxSuiteTestSuite
from app.services.tuxsuite_service import run_tuxsuite_tests
from app.core.config import settings
from sqlmodel import select
from fastapi import APIRouter, Request
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

router.post("/run-tests", status_code=204)
def run_tests(tests_data: TuxSuiteTestSuite, session: SessionDep, request: Request):
    """
    Schedules tests in tuxsuite.
    We only scheduledthe tests that have not been run for before for the build.
    """
    tests_has_been_run = session.exec(select(RunTest)
                                      .where(RunTest.build_id == tests_data.build_id)
                                      .where(RunTest.test_collection == tests_data.collection)).count()
    if tests_has_been_run > 0:
        logger.info(f"Test {tests_data.collection} has already been run for {tests_data.build_id}")
        return
    test_uid = run_tuxsuite_tests(tests_data.kernel_image_url, tests_data.modules_url, tests_data.tests, "qemu-riscv64",
                                  f"{settings.BASE_URL}{request.url_for("test_callback")}")
    scheduled_test = ScheduledTest(test_uid=test_uid, build_id=tests_data.build_id, collection=tests_data.collection)
    run_test = RunTest(build_id=tests_data.build_id, test_collection=tests_data.collection)
    session.add(run_test)
    session.add(scheduled_test)
    # Both queries are run in a transaction
    session.commit()
