"""
Services that handle re-trying failed submsissions.
They define their own router so they can be integrated into any app.

    from app.ap1.v1.endpoints import sync
    from fastapi import FastAPI

    app = FastAPI()
    app.include_router(sync.router)

"""
import logging
from app.core.db import SessionDep
from app.models.builds import RunBuild, mark_build_as_submitted
from app.models.tests import TestResults, mark_tests_as_submitted
from app.services.kcidb_services import submit_kcidb
from fastapi import APIRouter
from sqlmodel import select


router = APIRouter()

@router.post("/results", status_code=204)
async def sync_results(session: SessionDep):
    """
    Looks for unsubmitted test results and tries to submit them again.
    If the re try fails the results are kept stored, so that they can be submitted later.

    :param session: Database session. Used to access stored results
    """
    non_submitted_tests = session.exec(select(TestResults)).all()

    for test in non_submitted_tests:
        test_uid = test.test_uid
        results = test.results
        # Only submit results with submitted false
        logging.info(f"Submitting results for test uid {test_uid}")
        try:
            submit_kcidb(results)
            session.delete(test)
            mark_tests_as_submitted(test_uid, session)
            
        except:
            logging.warning(f"Could not submit results for test uid {test_uid}")
    session.commit()


@router.post("/builds", status_code=204)
async def sync_builds(session: SessionDep):
    """
    Looks for unsubmitted builds and tries to submit them again.
    If the re try fails the results are kept stored, so that they can be submitted later.

    :param session: Database session. Used to access stored results
    """
    non_submitted_builds = session.exec(select(RunBuild).where(RunBuild.submitted == False)).all()

    for build in non_submitted_builds:
        build_uid = build.build_uid
        submission = build.submission
        # Only submit results with submitted false
        logging.info(f"Submitting build for build uid {build_uid}")
        try:
            submit_kcidb([submission])
            mark_build_as_submitted(build_uid, session)
            
        except:
            logging.warning(f"Could not submit build with uid {build_uid}")
    session.commit()