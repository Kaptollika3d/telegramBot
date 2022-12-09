from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.session import DBSession
from aiogram_dialog import DialogManager

import db.queries


async def get_timetable(**kwargs):
    engine = create_engine("sqlite:///db/DB.db")
    session_factory = sessionmaker(bind=engine)
    db_session = DBSession(session_factory())
    times = db.queries.get_timetable(db_session)
    print(times)
    return {
      "times": times,
    }

async def get_clients_by_time(dialog_manager: DialogManager, **kwargs):
    engine = create_engine("sqlite:///db/DB.db")
    session_factory = sessionmaker(bind=engine)
    db_session = DBSession(session_factory())
    clients = db.queries.get_clients_by_time(db_session, dialog_manager.current_context().dialog_data.get("s_times"))
    return {
        "clients" : clients
    }