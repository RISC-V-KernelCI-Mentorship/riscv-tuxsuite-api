"""
Services to handle boot testing.
They define their own router so they can be integrated into any app.

    from app.ap1.v1.endpoints import boot
    from fastapi import FastAPI

    app = FastAPI()
    app.include_router(boot.router)

"""
from app.core.db import SessionDep
from app.core.runners import get_boot_callback_funcname, get_test_runner, get_test_callback_funcname
from app.models.tests import ScheduledTest, RunTest
from app.schemas.tests import BootTestSuite
from sqlmodel import func, select
from fastapi import APIRouter, Request
import logging

router = APIRouter()

@router.post("/run", status_code=204)
async def run_boot(tests_data: BootTestSuite, session: SessionDep, request: Request):
    """
    Schedules boot testing in a runner.
    We only scheduled tests that have not been run for before for the build.
    
    :param tests_data: Data required to run boot testing
    :param session: Database session
    :param request: Request object, allows us to obtain a URL from a function name
    """
    tests_has_been_run = session.exec(select(func.count(RunTest.build_id))
                                        .where(RunTest.build_id == tests_data.build_id)
                                        .where(RunTest.test == "boot")).one()
    if tests_has_been_run > 0:
        logging.info(f"Boot testing has already been been performed for {tests_data.build_id}")
        return

    tests_runner = get_test_runner(tests_data.runner)

    test_uid = tests_runner(tests_data.kernel_image_url, tests_data.modules_url,
                      ["boot"], "qemu-riscv64",
                      str(request.url_for(get_boot_callback_funcname(tests_data.runner))))
    scheduled_test = ScheduledTest(test_uid=test_uid, build_id=tests_data.build_id, test_collection="boot",
                                   tests=["boot"], runner=tests_data.runner)
    session.add(scheduled_test)
    run_test = RunTest(build_id=tests_data.build_id, test="boot")
    session.add(run_test)
    # Both queries are run in a transaction
    session.commit()
