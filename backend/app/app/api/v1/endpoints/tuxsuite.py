from typing import Annotated
from fastapi import APIRouter, Header
from app.models.tests import ScheduledTests
from app.schemas.tuxsuite import TuxSuiteTestRequest

router = APIRouter()


@router.post("/test-callback", status_code=204)
async def test_callback(x_tux_payload_signature: Annotated[str | None, Header()], request: TuxSuiteTestRequest):
    """
    Callback for tuxsuite test.
    It obtains the test from the database (to get its build id), stores the results in 
    the TestResults table and marks the test as finished.
    """
    print(x_tux_payload_signature)
    parsed_test_results = None
    # We o
    #body = await request.json()
    # It returns the results site in download_url, the you have to do
    # body[download_url]+ results.json
    # the json has the tests results
    print(request)
