from app.core.db import SessionDep
from app.models.tests import ScheduledTest, RunTest
from app.schemas.tuxsuite import TuxSuiteTestSuite
from app.services.tuxsuite_service import run_tuxsuite_tests
from app.core.config import settings
from sqlmodel import func, select
from fastapi import APIRouter, Request
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/run-tests", status_code=204)
async def run_tests(tests_data: TuxSuiteTestSuite, session: SessionDep, request: Request):
    """
    Schedules tests in tuxsuite.
    We only scheduledthe tests that have not been run for before for the build.
    """
    tests_to_run = []
    for test in tests_data.tests:
        tests_has_been_run = session.exec(select(func.count(RunTest.build_id))
                                        .where(RunTest.build_id == tests_data.build_id)
                                        .where(RunTest.test == test)).one()
        if tests_has_been_run > 0:
            logger.info(f"Test {test} from {tests_data.collection} has already been run for {tests_data.build_id}")
            continue
        tests_to_run.append(test)

    if len(tests_to_run) == 0:
        logger.info(f"No tests to run for build: {tests_data.build_id}")
        return

    test_uid = run_tuxsuite_tests(tests_data.kernel_image_url, tests_data.modules_url,
                                  tests_to_run, "qemu-riscv64",
                                  str(request.url_for("test_callback")))
    scheduled_test = ScheduledTest(test_uid=test_uid, build_id=tests_data.build_id, test_collection=tests_data.collection, tests=tests_to_run)
    session.add(scheduled_test)
    for test in tests_to_run:
        run_test = RunTest(build_id=tests_data.build_id, test=test)
        session.add(run_test)
    # Both queries are run in a transaction
    session.commit()
