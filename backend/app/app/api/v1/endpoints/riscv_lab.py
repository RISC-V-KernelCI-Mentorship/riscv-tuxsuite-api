from app.core.db import SessionDep
from app.models.tests import ScheduledTest, RunTest, TestResults
from app.schemas.test_results import RunnerTestsResults
from app.schemas.tuxsuite import TuxSuiteTestSuite
from app.services.runner_service import parse_results2kcidb
from app.services.tuxsuite_service import run_tuxsuite_tests
from app.services.kcidb_services import submit_tests
from app.utils.exceptions.tests_results_exceptions import TestSubmitionException
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


@router.post("/sync-results", status_code=204)
async def sync_results(session: SessionDep):
    non_submitted_tests = session.exec(select(TestResults)).all()
    for test in non_submitted_tests:
        test_uid = test.test_uid
        results = test.results
        logger.info(f"Submitting results for test uid {test_uid}")
        try:
            submit_tests(results)
            session.delete(test)
        except:
            logger.warning(f"Could not submit results for test uid {test_uid}")
    session.commit()


@router.post("/submit-results", status_code=204)
async def sync_results(results: RunnerTestsResults, session: SessionDep):
    logger.info(f"Received results for {results.test_uid}")
    test = session.exec(select(ScheduledTest).where(ScheduledTest.test_uid == results.test_uid)).one()
    parsed_results = parse_results2kcidb(results, test)
    json_results = [item.to_json() for item in parsed_results]
    
    try:
        submit_tests(json_results)
    except TestSubmitionException:
        test_row = TestResults(test_uid=results.test_uid, results=json_results)
        session.add(test_row)
        session.commit() 