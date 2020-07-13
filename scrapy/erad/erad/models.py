from sqlalchemy import Column, Date, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

CONNECTON_STRING = "mysql+pymysql://root:3wf5qnPbnA7q@mysql:3306/shikin?charset=utf8"
DeclarativeBase = declarative_base()


def db_connect():
    return create_engine(CONNECTON_STRING, echo=True)


def create_table(engine):
    DeclarativeBase.metadata.create_all(engine)


class FundDatabase(DeclarativeBase):
    __tablename__ = 'erad_erad'
    erad_key = Column(String(7), primary_key=True)
    url = Column(String(200))
    publishing_date = Column(Date())
    funding_agency = Column(String(200))
    call_for_applications = Column(String(200))
    application_unit = Column(String(200))
    approved_institution = Column(String(200))
    opening_date = Column(Date())
    closing_date = Column(Date())
