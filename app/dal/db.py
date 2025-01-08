from typing import Optional

from sqlmodel import Field, Session, SQLModel, create_engine, select

# Import Db Models that need creating
from dal.models import LogModel

class PostgresDb:

    def __init__(self, database_url: str):
        self.engine = create_engine(database_url)

        # Create if needed, based on imported models
        SQLModel.metadata.create_all(self.engine)

    def get_session(self):
        return Session(self.engine)


if __name__=='__main__':
    import os
    from datetime import datetime, timezone
    log = LogModel(
        sessionid="124", 
        userid="mafudge@syr.edu", 
        timestamp=datetime.now(timezone.utc).isoformat(), 
        role="user", 
        content="Hello, world!"
    )
    connnstr = os.environ["SQLALCHEMY_DATABASE_URL"]
    print(f"Connecting to {connnstr}")
    db = PostgresDb(database_url=connnstr)

    with db.get_session() as session:
        session.add(log)
        session.commit()

        statement = select(LogModel)
        item = session.exec(statement).first()
        print(item.model_dump())

