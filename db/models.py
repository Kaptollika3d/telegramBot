import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, TIMESTAMP, VARCHAR, ForeignKey, Table
from sqlalchemy.orm import relation, column_property

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    
    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    creted_at = Column(TIMESTAMP, nullable=False, default=datetime.datetime.now())
    updated_at = Column(TIMESTAMP, nullable=False, default=datetime.datetime.now(), onupdate=datetime.datetime.now())

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(id={self.id!r})>"

class Clients(BaseModel):
    __tablename__ = 'Clients'

    name = Column(VARCHAR(255), nullable=False)
    phone = Column(VARCHAR(255), nullable=False)
    description = Column(VARCHAR(255), nullable=True)
    status = Column(VARCHAR(100), nullable=True)

    def __repr__(self):
        return f'{self.name}'

    def __str__(self):
        return self.name

class Timetable(BaseModel):
    __tablename__ = 'Timetable'

    day_of_week = Column(VARCHAR(255), nullable=False)
    time = Column(VARCHAR(255), nullable=False)

    def __repr__(self):
        return f'{self.day, self.time}'

client_timetable = Table('client_timetable', Base.metadata,
    Column('client_id', Integer(), ForeignKey('Clients.id')),
    Column('timetable_id', Integer(), ForeignKey('Timetable.id'))
    )

class Payment(BaseModel):
    __tablename__ = 'PaidTrain'

    client_id = Column(ForeignKey("Clients.id"), nullable=False)
    number_paid_train = Column(Integer(), nullable=False) 

    def __repr__(self) -> str:
        return f'{self.client_id, self.number_paid_train}'

class Visits(BaseModel):
    __tablename__ = 'Visits'
    
    client_id = Column(ForeignKey("Clients.id"), nullable=False)
    timetable_id = Column(ForeignKey("Timetable.id"), nullable=False)

    def __repr__(self) -> str:
        return f'{self.client_id, self.timetable_id}'

class RemainTrain(BaseModel):
    __tablename__ = "RemainTrain"

    client_id = Column(ForeignKey("Clients.id"), nullable=False)
    available_train = Column(Integer(), nullable=False, default=0)

    def __repr__(self) -> str:
        return f'{self.client_id, self.available_train}'
