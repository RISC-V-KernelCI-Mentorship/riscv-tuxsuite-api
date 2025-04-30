
from app.core.db import SessionDep
from app.models.builds import ScheduledBuild
from app.schemas.builds import BuildData
from app.services.tuxsuite_service import run_tuxsuite_build
from fastapi import APIRouter, Request


router = APIRouter()
@router.post("/run", status_code=204)
def run_builds(build_data: BuildData, session: SessionDep, request: Request):
    """
    Submit a build request.
    The requests stores all the information requireed for the builds along with an identifier.
    """

    # Schedule the build
    build_uid = run_tuxsuite_build(build_data.toolchain, "riscv", build_data.tree, build_data.branch,
                                   build_data.kconfig, build_data.fragments,
                                  str(request.url_for("build_callback")))
    # Store it in the database
    scheduled_build = ScheduledBuild(build_uid=build_uid,
                                    toolchain=build_data.toolchain,
                                    tree=build_data.tree,
                                    branch=build_data.branch,
                                    kconfig=build_data.kconfig,
                                    fragments=build_data.fragments)
    session.add(scheduled_build)
    session.commit()
