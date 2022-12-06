from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.session import DBSession
from db.models import BaseModel
import db.queries

engine = create_engine("sqlite:///db/DB.db")
session_factory = sessionmaker(bind=engine)
db_session = DBSession(session_factory())

#db.queries.create_new_clients(db_session, "23", "232")
#db.queries.approve_new_clients(db_session, 1)
#db.queries.create_new_timetable(db_session, "Вторник", "18:00")
db.queries.create_new_visit(db_session, 1, 1)