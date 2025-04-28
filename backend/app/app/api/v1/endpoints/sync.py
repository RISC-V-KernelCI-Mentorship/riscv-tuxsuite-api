import logging
from app.core.db import SessionDep
from app.models.tests import TestResults, mark_test_as_submitted
from app.services.kcidb_services import submit_tests
from fastapi import APIRouter
from sqlmodel import select


router = APIRouter()

@router.post("/results", status_code=204)
async def sync_results(session: SessionDep):
    non_submitted_tests = session.exec(select(TestResults)).all()

    for test in non_submitted_tests:
        test_uid = test.test_uid
        results = test.results
        # Only submit results with submitted false
        logging.info(f"Submitting results for test uid {test_uid}")
        try:
            submit_tests(results)
            session.delete(test)
            mark_test_as_submitted(test_uid, session)
            
        except:
            logging.warning(f"Could not submit results for test uid {test_uid}")
    session.commit()