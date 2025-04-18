from typing import Annotated
from app.core.db import SessionDep
from app.services.kcidb_services import submit_tests
from app.services.tuxsuite_service import parse_tuxsuite2kcidb
from app.utils.exceptions.tests_results_exceptions import TestSubmitionException
from fastapi import APIRouter, Header
from app.models.tests import ScheduledTest, TestResults
from app.schemas.tuxsuite import TuxSuiteTestRequest
from sqlmodel import select
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/test-callback", status_code=204)
async def test_callback(x_tux_payload_signature: Annotated[str | None, Header()], request: TuxSuiteTestRequest,
                         session: SessionDep):
    """
    Callback for tuxsuite test.
    It obtains the test from the database (to get its build id), stores the results in 
    the TestResults table and marks the test as finished.
    """
    # TODO: add payload signature check
    tests_results = request.status
    logger.info(f"Received results for {tests_results.uid}")
    test = session.exec(select(ScheduledTest).where(ScheduledTest.test_uid == tests_results.uid)).one()
    parsed_test_results = await parse_tuxsuite2kcidb(tests_results, test)
    test_row = TestResults(test_uid=tests_results.uid, results={"results": [test.to_json() for test in parsed_test_results]})
    session.add(test_row)
    session.commit()
    try:
        submit_tests(parsed_test_results)
        session.delete(test_row)
        session.commit()
    except TestSubmitionException:
        pass 
