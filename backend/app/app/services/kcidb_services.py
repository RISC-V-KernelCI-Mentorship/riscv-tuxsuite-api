
from app.utils.exceptions.tests_results_exceptions import TestSubmitionException
from typing_extensions import Self
from datetime import datetime, timezone
from app.core.config import settings
import logging
import kcidb
import yaml
import os

logger = logging.getLogger(__name__)

class KCITestResultsSubmitter:

    def __init__(self):
        config_path = os.path.join(os.path.dirname(__file__), "kcidb.yml")
        with open(config_path, "r") as f:
            config_file = yaml.safe_load(f)
        self.__client = kcidb.Client(project_id=config_file["kcidb"]["project_id"],
                                     topic_name=config_file["kcidb"]["topic"])
        self.__version_major = config_file["kcidb"]["major"]
        self.__version_minor = config_file["kcidb"]["minor"]
        self.__debug = config_file["kcidb"]["is_debug"]


    def submit(self, tests):
        logger.info(f"Submitting tests: {tests}")
        report = {
            "tests": tests,
            "version": {
                "major": self.__version_major,
                "minor": self.__version_minor
            }
        }
        if self.__debug:
            logger.info(report)
        else:
            kcidb.io.SCHEMA.validate(report)            
            self.__client.submit(report)
            


class KCIDBTestSubmission:
    __origin = "riscv"

    def __init__(self, path: str, result: str, log: str, test_id: str, build_id: str) -> Self:
        self.__test_id = test_id
        self.__build_id = build_id
        self.__path = path
        self.__result = result
        self.__log = log
    

    def to_json(self):
        return {
                "id": f"{self.__origin}:{self.__test_id}",
                "build_id": self.__build_id,
                "origin": self.__origin,
                "status": self.__result,
                "path": self.__path,
                "start_time": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
                "misc": {}
            }


_submitter = KCITestResultsSubmitter()


def submit_tests(tests: list[dict]):
    try:
        _submitter.submit(tests)
    except Exception as e:
        logger.error(f"Could not validate submission!: {str(e)}")
        raise TestSubmitionException()