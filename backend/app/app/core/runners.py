
from app.services.tuxsuite_service import run_tuxsuite_tests, run_tuxsuite_build
from app.utils.exceptions.runner_exceptions import RunnerNotSupported


def get_test_runner(runner: str):
    match runner:
        case 'tuxsuite':
            return run_tuxsuite_tests
        case _:
            raise RunnerNotSupported(runner)
        
        
def get_build_runner(runner: str):
    match runner:
        case 'tuxsuite':
            return run_tuxsuite_build
        case _:
            raise RunnerNotSupported(runner)


def get_test_callback_funcname(runner: str):
    match runner:
        case 'tuxsuite':
            return 'tuxsuite_test_callback'
        case _:
            raise RunnerNotSupported(runner)


def get_build_callback_funcname(runner: str):
    match runner:
        case 'tuxsuite':
            return 'tuxsuite_build_callback'
        case _:
            raise RunnerNotSupported(runner)
