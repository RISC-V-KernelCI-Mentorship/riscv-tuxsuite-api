from fastapi import APIRouter
from app.schemas.request_schema import TuxSuiteTestSuite
from app.services.tuxsuite import run_tuxsuite_tests


router = APIRouter()

router.post("/run-tests", status_code=204)
def run_tests(tests_data: TuxSuiteTestSuite):
    run_tuxsuite_tests(tests_data.kernel_image_url, tests_data.modules_url, tests_data.tests, "qemu-riscv64")
    # TODO: register uuid and build id together so we can submit results to kcidb later