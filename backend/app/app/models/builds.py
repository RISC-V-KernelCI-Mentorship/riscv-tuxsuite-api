
from datetime import UTC, datetime
import logging
from typing import Optional
from app.core.db import SessionDep
from app.schemas.tuxsuite import TuxSuiteBuildStatus
from app.services.kcidb_services import KCIDBuildSubmission
from sqlmodel import JSON, Column, Field, SQLModel, select, update


class ScheduledBuild(SQLModel, table=True):
    __tablename__ = "scheduled_build"

    build_uid: str = Field(primary_key=True)
    toolchain: str
    tree: str
    branch: str
    kconfig: Optional[str] = None
    fragments: list[str] = Field(sa_column=Column(JSON), default=[])
    scheduled_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class RunBuild(SQLModel, table=True):
    __tablename__ = "run_build"

    build_uid: str = Field(foreign_key="scheduled_build.build_uid", primary_key=True)
    status: str
    submission: dict = Field(sa_column=Column(JSON), default=None)
    submitted: bool = Field(default=False)


class BuildArtifacts(SQLModel, table=True):
    __tablename__ = "build_artifact"

    build_uid: str = Field(foreign_key="scheduled_build.build_uid", primary_key=True)
    kernel_image: str
    modules: Optional[str] = Field(default=None)
    kernel_version: str


def mark_build_as_submitted(build_uid: str, session: SessionDep):
    session.exec(update(RunBuild)
                                 .where(RunBuild.build_uid == build_uid)
                                 .values(submitted=True))
    session.commit()
    logging.info(f"Marked build {build_uid} as submitted")


def store_build_result(build: TuxSuiteBuildStatus, build_submission: KCIDBuildSubmission, session: SessionDep):
    run_build = RunBuild(build_uid=build.uid, status=build.build_status, submission=build_submission.to_json())
    kernel_url = f"{build.download_url}{build.kernel_image_name}"
    artifacts = BuildArtifacts(build_uid=build.uid, kernel_image=kernel_url, kernel_version=build.kernel_version)
    if build.modules:
        modules_url = f"{build.download_url}{build.modules}"
        artifacts.modules = modules_url
    session.add(run_build)
    session.add(artifacts)
    session.commit()
