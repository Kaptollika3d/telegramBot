from sqlalchemy import null
from .session import DBSession
from .models import Clients, RemainTrain, Timetable, client_timetable, Visits


def create_new_clients(session: DBSession, name, phone, description=None):
    newClient = Clients(name=name, phone=phone, description=description, status='new')
    session.add_model(newClient)
    session.commit_session()

def approve_new_clients(session: DBSession, client_id):
    client = session.query(Clients).filter(Clients.id==client_id).one()
    client.status = 'active'

    if session.query(RemainTrain).filter(RemainTrain.client_id==client_id).one() is None:
        newRemainTrain = RemainTrain(client_id=client_id)
        session.add_model(newRemainTrain)

    session.commit_session()

#def set_client_timetable(session: DBSession, client_id, timetable_id):
#    newClientTimetable = client_timetable()


def create_new_timetable(session: DBSession, day_of_week, time):
    newTimetable = Timetable(day_of_week=day_of_week, time=time)
    session.add_model(newTimetable)
    session.commit_session()

def create_new_visit(session: DBSession, client_id, timetable_id):
    newVisit = Visits(client_id=client_id, timetable_id=timetable_id)
    session.add_model(newVisit)
    session.commit_session()

def get_timetable(session: DBSession):
    timetables = session.query(Timetable.id, Timetable.day_of_week, Timetable.time).all()
    dict = []
    for row in timetables:
        add = (row.id, "{0}, {1}".format(row.day_of_week, row.time))
        dict.append(add)
    return dict