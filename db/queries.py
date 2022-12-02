from sqlalchemy import null
from .session import DBSession
from .models import Clients


def create_new_clients(session: DBSession, name, phone, description=None):
    newClient = Clients(name=name, phone=phone, description=description, status='new')
    session.add_model(newClient)
    session.commit_session()