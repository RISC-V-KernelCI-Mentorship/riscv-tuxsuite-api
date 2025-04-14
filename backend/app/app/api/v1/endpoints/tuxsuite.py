from typing import Annotated
from fastapi import APIRouter, Header

from app.schemas.request_schema import TuxSuiteTestRequest

router = APIRouter()


@router.post("/test-callback", status_code=204)
async def test_callback(x_tux_payload_signature: Annotated[str | None, Header()], request: TuxSuiteTestRequest):
    """
    Callback for tuxsuite test 
    """
    print(x_tux_payload_signature)
    #body = await request.json()
    # It returns the results site in download_url, the you have to do
    # body[download_url]+ results.json
    # the json has the tests results
    print(request)
