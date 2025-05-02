from typing import Annotated
from app.core.db import SessionDep
from app.models.builds import ScheduledBuild, mark_build_as_submitted, store_build_result
from app.services.kcidb_services import submit_kcidb
from app.services.tuxsuite_service import parse_tuxsuite_build2kcidb, parse_tuxsuite_test2kcidb
from app.utils.exceptions.tests_results_exceptions import KCIDBSubmitionException
from fastapi import APIRouter, HTTPException, Header, Request, Response
from app.models.tests import ScheduledTest, TestResults, get_already_submitted_tests,\
    mark_as_received_tests_results, mark_test_as_submitted
from app.schemas.tuxsuite import TuxSuiteBuildRequest, TuxSuiteTestRequest
from sqlmodel import select
import logging
import sqlalchemy


router = APIRouter()


@router.post("/test", status_code=204)
async def test_callback(x_tux_payload_signature: Annotated[str | None, Header()], request: TuxSuiteTestRequest,
                         session: SessionDep):
    """
    Callback for tuxsuite test.
    It obtains the test from the database (to get its build id), stores the results in 
    the TestResults table and marks the test as finished.
    """
    # TODO: add payload signature check
    tests_results = request.status
    logging.info(f"Received results for {tests_results.uid}")
    test = session.exec(select(ScheduledTest).where(ScheduledTest.test_uid == tests_results.uid)).one()
    build_id = test.build_id
    # We mark the all tests from that test suit as received
    # TODO: Check how many of these are left as non-received and for how long
    mark_as_received_tests_results(tests_results.uid, session)
    submitted_tests = get_already_submitted_tests(build_id, tests_results.tests, session)
    parsed_test_results = await parse_tuxsuite_test2kcidb(tests_results, test, submitted_tests)
    results = [item.to_json() for item in parsed_test_results]
    
    try:
        # Only submit results with submitted false
        submit_kcidb(results)
        mark_test_as_submitted(tests_results.uid, session)
    except KCIDBSubmitionException:
        test_row = TestResults(test_uid=tests_results.uid, build_id=build_id ,results=results)
        session.add(test_row)
        session.commit() 


@router.post("/build", status_code=204)
async def build_callback(x_tux_payload_signature: Annotated[str | None, Header()], request: TuxSuiteBuildRequest,
                         session: SessionDep):
    """
    Callback for tuxsuite build.
    It obtains the build from the database, and marks its completion state.
    If it passed the build we submit it to KCIDB
    """
    # TODO: add payload signature check
    build_results = request.status
    logging.info(f"Received build results for {build_results.uid}")
    try:
        build = session.exec(select(ScheduledBuild).where(ScheduledBuild.build_uid == build_results.uid)).one()
    except sqlalchemy.exc.NoResultFound:
        logging.warning(f"Received unexpected build uid: {build_results.uid}")
        raise HTTPException(status_code=500, detail=f"Invalid build uid {build_results.uid}")
    
    parsed_build_result = await parse_tuxsuite_build2kcidb(build_results, build)
    store_build_result(build_results, parsed_build_result, session)
    
    try:
        submit_kcidb([parsed_build_result.to_json()])
        mark_build_as_submitted(build_uid=build_results.uid, session=session)
    except KCIDBSubmitionException:
        logging.warning(f"Build {build_results.uid} couldn't be submitted")
    