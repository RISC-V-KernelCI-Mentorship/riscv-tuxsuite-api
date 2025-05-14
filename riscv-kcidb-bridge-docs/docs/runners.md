# Runners

We define a runner as a mechanism for running tests and/or builds. As shown in the [diagram](index.md#sytem-design) in the home, we assume the runners will work asynchronously. This means we will schedule builds, tests and boot tests and the runner will notify their completion.

Furthermore, we assume that each runner accepts a URL as a callback, and that it performs a `POST HTTP` request when it finishes running.

Depending on the use of the runner you'll need to either define a `TestRunner`, a `BuildRunner` or both.

By default we have implemented a [TuxSuite](https://tuxsuite.com/home) runner, which runs both tests and builds.

## Locating runners

All available runners can be found in the [`runners.py`](https://github.com/RISC-V-KernelCI-Mentorship/riscv-kcidb-bridge/blob/main/backend/app/app/core/runners.py) file, under the `AVAILABLE_RUNNERS` type.

This list is kept as an easy way to access the codes for all available runners.

## Defining new runners

For each runner you need to define a code, a function to schedule tests or builds, and a set of callbacks.

### 1. Defining a code

The code should be unique and be included in the `AVAILABLE_RUNNERS` in [`runners.py`](https://github.com/RISC-V-KernelCI-Mentorship/riscv-kcidb-bridge/blob/main/backend/app/app/core/runners.py).

For example, we can see that the TuxSuite runner has `tuxsuite` as a code.

### 2. Schedule tests and boot tests

A test scheduler is any kind of callable that follows the [`TestRunner` protocol](https://github.com/RISC-V-KernelCI-Mentorship/riscv-kcidb-bridge/blob/main/backend/app/app/core/runners.py#L8). This can be used to schedule both tests and boot tests.

This callable needs to send the test to the runner service, and return a unique identifier for the operation. This id will used when the callback is called to identify which operation was completed.
Storing the identifier allows you to schedule multiple tests at once, even if the order in which they finished is different from how they were scheduled.

The scheduler need to be defined in any module accesible by [`runners.py`](https://github.com/RISC-V-KernelCI-Mentorship/riscv-kcidb-bridge/blob/main/backend/app/app/core/runners.py). For example, for the TuxSuite runner we define the test scheduler in [`tuxsuite_service.py`](https://github.com/RISC-V-KernelCI-Mentorship/riscv-kcidb-bridge/blob/main/backend/app/app/services/tuxsuite_service.py#L13).

After creating it, the scheduler it needs to be added to the [`runners.py`](https://github.com/RISC-V-KernelCI-Mentorship/riscv-kcidb-bridge/blob/main/backend/app/app/core/runners.py#L43) file, under the `get_test_runner` function.

For example, let's assume we're adding a new `demo` runner. Integrating this runner could look like this:

```python
AVAILABLE_RUNNERS = Literal['tuxsuite', 'demo']

def get_test_runner(runner: str) -> TestRunner:
    match runner:
        case 'tuxsuite':
            return run_tuxsuite_tests
        # We add a new case for the demo runner
        case 'build':
            # demo_test_runner is implemented elsewhere and imported
            return demo_test_runner
        case _:
            raise RunnerNotSupported(runner)
```

### 3. Schedule builds

A build scheduler is a callable that complies to the [`BuildRunner`protocol](https://github.com/RISC-V-KernelCI-Mentorship/riscv-kcidb-bridge/blob/main/backend/app/app/core/runners.py#L24).

Build schedulers similarly to test schedulers, meaning they must return a unique identifier representing the build operation.

For TuxSuite, the build runner can be found in [`tuxsuite_service.py`](https://github.com/RISC-V-KernelCI-Mentorship/riscv-kcidb-bridge/blob/main/backend/app/app/services/tuxsuite_service.py#L27).

After creating it, the scheduler it needs to be added to the [`runners.py`](https://github.com/RISC-V-KernelCI-Mentorship/riscv-kcidb-bridge/blob/main/backend/app/app/core/runners.py#L87) file, under the `get_build_runner` function.

For example, adding a new `demo` build runner could look like this:

```python
AVAILABLE_RUNNERS = Literal['tuxsuite', 'demo']

def get_build_runner(runner: str) -> BuildRunner:
    match runner:
        case 'tuxsuite':
            return run_tuxsuite_build
        # We add a new case for the demo runner
        case 'demo':
            # demo_build_runner is implemented elsewhere and imported
            return demo_build_runner
        case _:
            raise RunnerNotSupported(runner)
```

### 4. Test, boot test and build callbacks

Test and build callbacks are `REST` services that need to comply to the requirements of each runner.

For instance, [TuxSuite callbacks](https://docs.tuxsuite.com/callbacks/) expect a `x-tux-payload-signature` header used to verify the origin of the request.

There are several steps to defining the callbacks:

#### a. Define the schemas

The schemas represente the body of the requests. They are used by [`pydatinc`](https://docs.pydantic.dev/latest/concepts/models/) to verify the body of the request is valid.

Each runner might have a different schema. It is the responsability of the person adding the new runner to verify what the body of the callback request looks like.

For example, for the `tuxsuite` runner we define the `TuxSuiteTestRequest` and the `TuxSuiteBuildRequest` models in the [`tuxsuite.py`](https://github.com/RISC-V-KernelCI-Mentorship/riscv-kcidb-bridge/blob/main/backend/app/app/schemas/tuxsuite.py) file. These follow the structure described in [TuxSuite's documentation](https://docs.tuxsuite.com/callbacks/).

#### b. Create the services

A new file should be added to the `backend/app/app/api/v1/endpoints` folder. This file will contain the definition of all the necessary callbacks.

For a runner with code `demo` the basic structure of the file might look as follows:

```python
from typing import Annotated
from app.core.db import SessionDep
from fastapi import APIRouter, Header
from app.schemas.demo import DemoBuildRequest, DemoTestRequest

# Create a fast api router for the services
router = APIRouter()

# Test callback, the status code we return depends on what the runner expects
@router.post("/test", status_code=204)
async def demo_test_callback(x_demo_header: Annotated[str | None, Header()], request: DemoTestRequest, session: SessionDep):
    """
    Callback for demo runner tests.
    Args:
        :x_demo_header (str): An example header. To obtain any other header from the request you just need to add an extra parameter to the function
        :request (DemoTestRequest): This is the model defined in the previous step.
        :session (SessionDep): Gives you access to the database
    """
    ...

# Build callback, the status code we return depends on what the runner expects
@router.post("/build", status_code=204)
async def demo_build_callback(x_demo_header: Annotated[str | None, Header()], request: DemoBuildRequest, session: SessionDep):
    """
    Callback for demo runner builds.
    Args:
        :x_demo_header (str): An example header. To obtain any other header from the request you just need to add an extra parameter to the function
        :request (DemoBuildRequest): This is the model defined in the previous step.
        :session (SessionDep): Gives you access to the database
    """
    ...

@router.post("/boot", status_code=204)
async def demo_boot_callback(x_tux_payload_signature: Annotated[str | None, Header()], request: TuxSuiteTestRequest,
                         session: SessionDep):
    """
    Callback for demo boot test.

    :x_demo_header (str): An example header. To obtain any other header from the request you just need to add an extra parameter to the function
    :request (DemoTestRequest): This is the model defined in the previous step.
    :session (SessionDep): Gives you access to the database

    """
    ...
```

Please make sure that the names of the functions are unique inside the project.

#### c. Add the services to the main router

The services will only be visible after they're added to the main app router. To do so you need to modify the [`backend/app/app/api/v1/api.py` file](https://github.com/RISC-V-KernelCI-Mentorship/riscv-kcidb-bridge/blob/main/backend/app/app/api/v1/api.py).

For the `demo` runner it could look as follows:

```python
from fastapi import APIRouter
from app.api.v1.endpoints import (
    builds, tests, sync, tuxsuite_callbacks, demo
)

api_router = APIRouter()
# These are all the existing paths
api_router.include_router(tuxsuite_callbacks.router, prefix="/tuxsuite/callback", tags=["tuxsuite callbacks"])
api_router.include_router(tests.router, prefix="/tests", tags=["tests"])
api_router.include_router(builds.router, prefix="/builds", tags=["builds"])
api_router.include_router(sync.router, prefix="/sync", tags=["sync"])
api_router.include_router(boot.router, prefix="/boot", tags=["boot"])
# We include the demo router here
api_router.include_router(sync.router, prefix="/demo/callback", tags=["demo callbacks"])
```

After this the services under `/demo/callback/test`, `/demo/callback/boot`, and `/demo/callback/build` will be callable from the runner.

### 5. Configuring callback names

By now you should now that `TestRunner` and `BuildRunner` have a callback name as a parameter.
Instead of passing the strings directly we define a couple of functions that allow centralizing obtaining the names.

Both functions are located in the [`runners.py` file](https://github.com/RISC-V-KernelCI-Mentorship/riscv-kcidb-bridge/blob/main/backend/app/app/core/runners.py).
To add a test callback name for a new `demo` runner you need to modify the `get_test_callback_funcname` function:

```python
def get_test_callback_funcname(runner: str) -> str:
    match runner:
        case 'tuxsuite':
            return 'tuxsuite_test_callback'
        case 'demo':
            # This is the name of the function we defined at test callback
            return 'demo_test_callback'
        case _:
            raise RunnerNotSupported(runner)
```

For a build callback name for a new `demo` runner you need to modify the `get_build_callback_funcname` function:

```python
def get_build_callback_funcname(runner: str) -> str:
    match runner:
        case 'tuxsuite':
            return 'tuxsuite_build_callback'
        case 'demo':
            # This is the name of the function we defined at build callback
            return 'demo_build_callback'
        case _:
            raise RunnerNotSupported(runner)
```

Finally, for a boot callback name for a new `demo` runner you need to modify the `get_boot_callback_funcname` function:

```python
def get_boot_callback_funcname(runner: str) -> str:
    match runner:
        case 'tuxsuite':
            return 'tuxsuite_boot_callback'
        case 'demo':
            # This is the name of the function we defined at boot callback
            return 'demo_boot_callback'
        case _:
            raise RunnerNotSupported(runner)
```
