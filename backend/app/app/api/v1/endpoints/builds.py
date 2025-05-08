"""
Services to handle build runs.
They define their own router so they can be integrated into any app.

    from app.ap1.v1.endpoints import builds
    from fastapi import FastAPI

    app = FastAPI()
    app.include_router(builds.router)

"""
from app.core.db import SessionDep
from app.core.runners import get_build_callback_funcname, get_build_runner
from app.models.builds import ScheduledBuild
from app.schemas.builds import BuildData
from fastapi import APIRouter, Request


router = APIRouter()
@router.post("/run", status_code=204)
def run_builds(build_data: BuildData, session: SessionDep, request: Request):
    """
    Submit a build request.
    The requests stores all the information requireed for the builds along with an identifier.

    :param build_data: Data required by runners to perform a build
    :param session: Database session
    :param request: Request object
    """
    build_runner = get_build_runner(build_data.runner)
    # Schedule the build
    build_uid = build_runner(build_data.toolchain, "riscv", build_data.tree, build_data.branch,
                             build_data.kconfig, build_data.fragments,
                             str(request.url_for(get_build_callback_funcname(build_data.runner))))
    # Store it in the database
    scheduled_build = ScheduledBuild(build_uid=build_uid,
                                    toolchain=build_data.toolchain,
                                    tree=build_data.tree,
                                    branch=build_data.branch,
                                    kconfig=build_data.kconfig,
                                    fragments=build_data.fragments,
                                    runner=build_data.runner)
    session.add(scheduled_build)
    session.commit()
