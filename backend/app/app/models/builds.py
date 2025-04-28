
from typing import Optional
from sqlmodel import JSON, Column, Field, SQLModel


class ScheduledBuild(SQLModel, table=True):
    __tablename__ = "scheduled_build"

    build_uid: str = Field(primary_key=True)
    toolchain: str
    tree: str
    branch: str
    kconfig_url: Optional[str] = None
    fragments: list[str] = Field(sa_column=Column(JSON), default=[])


class RunBuild(SQLModel, table=True):
    build_uid: str = Field(foreign_key="scheduled_build.build_uid")
    status: str
    submitted: bool = Field(default=False)
