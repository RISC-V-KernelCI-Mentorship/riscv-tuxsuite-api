
from typing import Callable, Optional, Protocol
from app.services.tuxsuite_service import run_tuxsuite_tests, run_tuxsuite_build
from app.utils.exceptions.runner_exceptions import RunnerNotSupported

AVAILABLE_RUNNERS = ['tuxsuite']

class TestRunner(Protocol):
    def __call__(self, kernel_url: str, modules_url: Optional[str], tests: list[str], device: str, callback: str) -> str:
        '''
        Describes the expected signature of a tests runner
        Args:
            :kernel_url (str): Built kernel image URL
            :modules_url (Optional[str]): Built modules URL. They need to be compressed in a single file
            :tests (list[str]): List of tests to run. Support may vary from runner to runner
            :device (str): The device used to run the tests
            :callback (str): The name of the callback function
        
        Returns
            str: a unique identifier representing the scheduled tests
        '''
        ...
    
class BuildRunner(Protocol):
    def __call__(self, toolchain: str, arch: str, tree: str, branch: str, kconfig: Optional[str], fragments: list[str], callback: str) -> str:
        '''
        Describes the expected signature of a tests runner
        Args:
            :toolchain (str): Used when compiling. Support may vary depending on the
            :arch (str): Target architecture
            :tree (str): Git repo of the tree to build
            :branch (str): Branch to consider
            :kconfig (Optional[str]): URL to a kconfig file, or predefined kernel configuration (e.g. defconfig)
            :fragments (list[str]): List of fragments to use
            :callback (str): The name of the callback function
        
        Returns
            str: a unique identifier representing the scheduled build
        '''
        ...
    

def get_test_runner(runner: str) -> TestRunner:
    '''
    Returns the test scheduler for a given runner. The returned function is expected
    to have a specific signature:
    runner(kernel_url: str, modules_url: Optional[str], tests: list[str], device: str, callback: str) -> str

    Args:
        :runner (str): The code of the runner
    
    Returns:
        Runner: returns the runner function
    
    Raises:
        RunnerNotSupported: when passed a runner that has not been implemented yet
    '''
    match runner:
        case 'tuxsuite':
            return run_tuxsuite_tests
        case _:
            raise RunnerNotSupported(runner)
        
        
def get_build_runner(runner: str) -> BuildRunner:
    '''
    Returns the build scheduler for a given runner. The returned function is expected
    to have a specific signature:
    runner(toolchain: str, arch: str, tree: str, branch: str, kconfig: Optional[str], fragments: list[str], callback: str)) -> str

    Args:
        :runner (str): The code of the runner
    
    Returns:
        Runner: returns the runner function
    
    Raises:
        RunnerNotSupported: when passed a runner that has not been implemented yet
    '''
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
