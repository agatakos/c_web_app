import os
from app import db
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, String, MetaData


Base = automap_base()

engine = create_engine(
    "postgresql://postgres:postgres@localhost:5432/Cuvva Tech Assesment"
)
Base.prepare(engine, reflect=True)


# match postgres tables
Policy = Base.classes.policy
Finance = Base.classes.finance
Calendar = Base.classes.calendar

# match views
metadata = MetaData()
Policy_Day = Table("policy_status_daily", metadata, autoload_with=engine)
User_Month = Table("user_status_monthly", metadata, autoload_with=engine)


session = Session(engine)
session.commit()


def __init__(self, name):
    """initialize with name."""
    self.name = name


def save(self):
    db.session.add(self)
    db.session.commit()


@staticmethod
def get_all():
    return db.session.query(Policy).query.all()


def delete(self):
    db.session.delete(self)
    db.session.commit()


def __repr__(self):
    return "".format(self.name)


if __name__ == "__main__":
    from sqlalchemy.orm import scoped_session, sessionmaker, Query

    db_session = scoped_session(sessionmaker(bind=engine))
    for item in db_session.query(Policy.policy_id, Policy.user_id):
        print(item)
    for item in db_session.query(
        Finance.finance_transaction_id, Finance.policy_id
    ):
        print(item)
