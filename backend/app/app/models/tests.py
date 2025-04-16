from sqlmodel import JSON, Column, Field, SQLModel, create_engine

class ScheduledTests(SQLModel, table=True):
    __tablename__ = "scheduled_tests"

    test_uid: str = Field(primary_key=True)
    build_id: str


class TestResults(SQLModel, table=True):
    __tablename__ = "test_results"

    id: int | None = Field(default=None, primary_key=True)
    test_uid: str = Field(foreign_key="scheduled_tests.test_uid")
    results: dict = Field(sa_column=Column(JSON))


class FinishedTests(SQLModel, table=True):
    __tablename__ = "finished_tests"

    build_id: str = Field(primary_key=True)
    test_uid: str = Field(primary_key=True)


if __name__ == "__main__":
    sqlite_file_name = "database.db"
    sqlite_url = f"sqlite:///{sqlite_file_name}"

    connect_args = {"check_same_thread": False}
    engine = create_engine(sqlite_url, connect_args=connect_args)
    SQLModel.metadata.create_all(engine)
