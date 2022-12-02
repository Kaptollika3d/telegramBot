import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, TIMESTAMP, VARCHAR, ForeignKey
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

