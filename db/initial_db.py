from sqlalchemy import create_engine

from models import BaseModel, Base

engine = create_engine("sqlite:///DB.db")
engine.connect()

Base.metadata.create_all(engine)

print(engine)