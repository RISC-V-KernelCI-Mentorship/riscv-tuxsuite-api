from app.models.tests import ScheduledTest
from app.schemas.tuxsuite import TuxSuiteTestStatus
from app.services.kcidb_services import KCIDBTestSubmission
from app.utils.exceptions.tests_results_exceptions import DownloadResultsException, InvalidResultsException
import logging
from app.utils.test_parser import generate_test_id, get_test_path
import tuxsuite
import argparse
import httpx

def run_tuxsuite_tests(kernel_url: str, modules_url: str | None, tests: list[str], device: str, callback: str) -> str:
    params = {
        "device": device,
        "kernel": kernel_url,
        "tests": tests,
        "callback": callback
    }
    if modules_url is not None:
        params["modules"] = modules_url
    test = tuxsuite.Test(**params)
    test.test()
    uid = test.uid
    return uid

async def parse_tuxsuite2kcidb(tests_results: TuxSuiteTestStatus, stored_test: ScheduledTest) -> list[KCIDBTestSubmission]:
    parsed_results = []
    logs_url = f"{tests_results.download_url}logs.txt"
    results_json_url = f"{tests_results.download_url}results.json"
    async with httpx.AsyncClient() as client:
        logs_response = await client.get(logs_url, follow_redirects=True)
        try:
            if not logs_response.is_redirect:
                logs_response.raise_for_status()
            logs = logs_response.text
        except:
            logs = ""
        results_response = await client.get(results_json_url, follow_redirects=True)
        try:
            if not results_response.is_redirect:
                results_response.raise_for_status()
            results = results_response.json()
        except:
            raise DownloadResultsException()
    if 'lava' not in results:
        raise InvalidResultsException()
    lava_info = results['lava']
    for test in tests_results.tests:
        if test not in lava_info:
            logging.warning(f"No results for {test}")
            continue
        path = get_test_path(stored_test.test_collection, test)
        test_id = generate_test_id(stored_test.test_uid, stored_test.test_collection, test)
        test_result = lava_info[test]['result'].upper()
        parsed_results.append(KCIDBTestSubmission(path,  test_result, logs, test_id, stored_test.build_id))
    
    return parsed_results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run tuxsuite test from the command line")
    parser.add_argument("--kernel-url", required=True, help="Kernel URL")
    parser.add_argument("--modules-url", default=None, help="Modules URL")
    parser.add_argument("--tests", required=True, action="append", help="Tests to run. Support multiple tests")
    args = parser.parse_args()

    device = "qemu-riscv64"
    test_uid = run_tuxsuite_tests(args.kernel_url, args.modules_url, args.tests, device)
    print(f"Test uid: {test_uid}")
