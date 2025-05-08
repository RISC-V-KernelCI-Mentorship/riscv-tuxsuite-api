"""
Services to handle tests runs and submissions.
They define their own router so they can be integrated into any app.

    from app.ap1.v1.endpoints import tests
    from fastapi import FastAPI

    app = FastAPI()
    app.include_router(tests.router)

"""
from app.core.db import SessionDep
from app.core.runners import get_test_runner, get_test_callback_funcname
from app.models.tests import ScheduledTest, RunTest, TestResults
from app.schemas.tests import RunnerTestsResults, TestSuite
from app.services.runner_service import parse_results2kcidb
from app.services.kcidb_services import submit_kcidb
from app.utils.exceptions.tests_results_exceptions import KCIDBSubmitionException
from sqlmodel import func, select
from fastapi import APIRouter, Request
import logging

router = APIRouter()

@router.post("/run", status_code=204)
async def run_tests(tests_data: TestSuite, session: SessionDep, request: Request):
    """
    Schedules tests in a runner.
    We only scheduled tests that have not been run for before for the build.
    
    :param tests_data: Tests to schedule
    :param session: Database session
    :param request: Request object, allows us to obtain a URL from a function name
    """
    tests_to_run = []
    for test in tests_data.tests:
        tests_has_been_run = session.exec(select(func.count(RunTest.build_id))
                                        .where(RunTest.build_id == tests_data.build_id)
                                        .where(RunTest.test == test)).one()
        if tests_has_been_run > 0:
            logging.info(f"Test {test} from {tests_data.collection} has already been run for {tests_data.build_id}")
            continue
        tests_to_run.append(test)

    if len(tests_to_run) == 0:
        logging.info(f"No tests to run for build: {tests_data.build_id}")
        return

    tests_runner = get_test_runner(tests_data.runner)

    test_uid = tests_runner(tests_data.kernel_image_url, tests_data.modules_url,
                      tests_to_run, "qemu-riscv64",
                      str(request.url_for(get_test_callback_funcname(tests_data.runner))))
    scheduled_test = ScheduledTest(test_uid=test_uid, build_id=tests_data.build_id, test_collection=tests_data.collection,
                                   tests=tests_to_run, runner=tests_data.runner)
    session.add(scheduled_test)
    for test in tests_to_run:
        run_test = RunTest(build_id=tests_data.build_id, test=test)
        session.add(run_test)
    # Both queries are run in a transaction
    session.commit()



@router.post("/submit", status_code=204)
async def submit_results(results: RunnerTestsResults, session: SessionDep):
    """
    Submit test results to KCIDB. In this case test runner is not relevant.

    :param results: Test results passed as the body of the request
    :param session: Database session
    """
    logging.info(f"Received results for {results.test_uid}")
    parsed_results = parse_results2kcidb(results)
    json_results = [item.to_json() for item in parsed_results]
    
    try:
        submit_kcidb(json_results)
    except KCIDBSubmitionException:
        test_row = TestResults(test_uid=results.test_uid, build_id=results.build_id, results=json_results)
        session.add(test_row)
        session.commit() 
