import logging
from datetime import datetime, UTC
from app.core.db import SessionDep
from sqlmodel import JSON, Column, Field, SQLModel, create_engine, select, update

class ScheduledTest(SQLModel, table=True):
    __tablename__ = "scheduled_tests"

    test_uid: str = Field(primary_key=True)
    build_id: str
    test_collection: str
    tests: list[str] = Field(sa_column=Column(JSON))
    scheduled_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    runner: str


class TestResults(SQLModel, table=True):
    __tablename__ = "test_results"

    id: int | None = Field(default=None, primary_key=True)
    test_uid: str = Field(foreign_key="scheduled_tests.test_uid")
    build_id: str
    results: dict = Field(sa_column=Column(JSON))


class RunTest(SQLModel, table=True):
    __tablename__ = "run_tests"

    build_id: str = Field(primary_key=True)
    test: str = Field(primary_key=True)
    ran_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    received_results: bool = Field(default=False)
    submitted_results: bool = Field(default=False)



def mark_tests_as_submitted(tests: list[str], build_uid: str, session: SessionDep):
    for test in tests:
        run_test = session.exec(select(RunTest)
                                .where(RunTest.build_id == build_uid)
                                .where(RunTest.test == test)).one()
        run_test.submitted_results = True
        session.add(run_test)
    session.commit()
    logging.info(f"Marked tests {tests} as submitted")


def mark_as_received_tests_results(tests: list[str], build_uid: str, session: SessionDep):
    for test in tests:
        run_test = session.exec(select(RunTest)
                                .where(RunTest.build_id == build_uid)
                                .where(RunTest.test == test)).one()
        run_test.received_results = True
        session.add(run_test)
    session.commit()
    logging.info(f"We recieved results for tests {tests}")


def get_already_submitted_tests(build_id: str, tests: list[str], session: SessionDep):
    submitted_tests = session.exec(select(RunTest)
                                   .where(RunTest.submitted_results == True)
                                   .where(RunTest.received_results == True)
                                   .where(RunTest.test.in_(tests))
                                   .where(RunTest.build_id == build_id)).all()
    return submitted_tests


if __name__ == "__main__":
    sqlite_file_name = "database.db"
    sqlite_url = f"sqlite:///{sqlite_file_name}"

    connect_args = {"check_same_thread": False}
    engine = create_engine(sqlite_url, connect_args=connect_args)
    SQLModel.metadata.create_all(engine)
