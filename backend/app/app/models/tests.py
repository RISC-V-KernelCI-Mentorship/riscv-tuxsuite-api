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



def mark_test_as_submitted(test_uid: str, session: SessionDep):
    updated_tests = session.exec(update(TestResults, RunTest)
                                         .set(RunTest.submitted_results == True)
                                         .where(RunTest.submitted_results == False)
                                         .where(RunTest.received_results == True)
                                         .where(TestResults.build_id == RunTest.build_id)
                                         .where(TestResults.test_uid == test_uid))
    logging.info(f"Updated {updated_tests} tests for test {test_uid}")


def mark_as_received_tests_results(test_uid: str, session: SessionDep):
    updated_tests = session.exec(update(TestResults, RunTest)
                                         .set(RunTest.received_results == True)
                                         .where(RunTest.received_results == False)
                                         .where(TestResults.build_id == RunTest.build_id)
                                         .where(TestResults.test_uid == test_uid))
    logging.info(f"Updated {updated_tests} tests for test {test_uid}")


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
