from functools import lru_cache
from typing import Iterator
from uuid import UUID

import sqlalchemy as sa
import uvicorn as uvicorn
from fastapi import Depends, FastAPI
from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship
from sqlalchemy import Column, Boolean, Numeric, String, Date, DateTime, Text
from sqlalchemy import MetaData
from fastapi_utils.guid_type import GUID, GUID_DEFAULT_SQLITE
from fastapi_utils.session import FastAPISessionMaker

Base = declarative_base()



# Main Model representing a SSA Office
class Office(Base):
    __tablename__ = "ssoffices_ssoffice"  # TODO change this to ssa_office??

    id = Column(String, primary_key=True)
    slug = Column(String, index=True)
    display_name = Column(String, index=True)
    site_code = Column(String, index=True)  # TODO change this to ssa_site_code
    ssa_office_name = Column(String, index=True)
    ssa_last_updated = Column(Date, index=True)
    address1 = Column(String, index=True)
    address2 = Column(String, index=True)
    city = Column(String, index=True)
    state = Column(String, index=True)
    zipcode = Column(String, index=True)
    tel_public = Column(String, index=True)
    tel_call_back = Column(String, index=True)
    tel_admin = Column(String, index=True)
    fax = Column(String, index=True)
    notes = Column(Text, index=True)
    modified = Column(DateTime, index=True)
    efile_fax = Column(String, index=True)  # TODO: obsolete?
    latitude = Column(Numeric, index=True)
    longitude = Column(Numeric, index=True)
    servicing_fos = Column(String, index=True)
    servicing_states = Column(String, index=True)  # TDDO  simple comma delimited string?
    servicing_zipcodes = Column(String, index=True)  # TDDO  simple comma delimited string?
    region = Column(String, index=True)
    type = Column(String, index=True)

    # comments = relationship("OfficeComment", back_populates="office")
    # staff = relationship("OfficeStaff", back_populates="office")

class DBSettings(BaseSettings):
    """ Parses variables from environment on instantiation """

    database_uri: str="sqlite:///.sso.db"  # could break up into scheme, username, password, host, db


def get_db() -> Iterator[Session]:
    """ FastAPI dependency that provides a sqlalchemy session """
    yield from _get_fastapi_sessionmaker().get_db()


@lru_cache()
def _get_fastapi_sessionmaker() -> FastAPISessionMaker:
    """ This function could be replaced with a global variable if preferred """
    database_uri = DBSettings().database_uri
    return FastAPISessionMaker(database_uri)


app = FastAPI()


@app.get("/test")
def return_test() -> str:
    return "TEST RETURNED"



def get_offices(db: Session = Depends(get_db)) -> str:
    db.query()
    offices = db.query(Office).all()
    return offices


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7000)