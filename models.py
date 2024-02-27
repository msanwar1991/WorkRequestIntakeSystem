from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()


class WorkRequest(Base):
    # Table to store work requests
    __tablename__ = 'work_requests'
    # Columns
    id = Column(Integer, primary_key=True)
    request_detail = Column(String, nullable=False)
    equipment_name = Column(String, nullable=False)  
    station_name = Column(String, nullable=False) 
    date_condition_observed = Column(DateTime, nullable=False)
    spare_part_required = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    

    def update(self, session, **kwargs):
        try:
            # Update the object with the key-value pairs in kwargs
            for key, value in kwargs.items():
                setattr(self, key, value)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e

    def remove(self, session):
        try:
            # Remove the object from the database
            session.delete(self)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e

# SQLite database using SQLAlchemy
engine = create_engine('sqlite:///work_requests.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
