import add_path  # noqa: F401
from orm import engine,TaskResult
from sqlmodel import Session,select

with Session(engine) as session:
    statement = select(TaskResult)
    results = session.exec(statement)
    for i in results:
        print(i)
