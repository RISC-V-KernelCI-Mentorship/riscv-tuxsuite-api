from app.schemas.tests import RunnerTestsResults
from app.services.kcidb_services import KCIDBTestSubmission
from app.utils.test_parser import generate_test_id, get_test_path


async def parse_results2kcidb(tests_results: RunnerTestsResults) -> list[KCIDBTestSubmission]:
    parsed_results = []
    for test in tests_results.tests:
        path = get_test_path(test.test_collection, test)
        test_id = generate_test_id(tests_results.test_uid, test.test_collection, test.test_name)
        parsed_results.append(KCIDBTestSubmission(path, test.result, test.logs, test_id, tests_results.build_id))
    
    return parsed_results
