from sqlalchemy import BigInteger, create_engine, Column, DateTime, ForeignKey, Integer, Sequence, String, \
    UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

import json
import os

db_url = os.environ['SAVORY_DB_URL']
db = create_engine(db_url)
base = declarative_base()


# TODO: This is unused and may not be needed!
def model_to_json(model):
    d = {}
    for column in model.__table__.columns:
        d[column.name] = str(getattr(model, column.name))

    return json.dumps(d)


class Account(base):
    __tablename__ = 'account'

    id = Column(Integer, Sequence('account_id_seq', start=1, increment=1), primary_key=True)
    social_profile_id = Column(BigInteger, nullable=False)
    social_profile_type = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    profile_image = Column(String, nullable=False)
    creation_date = Column(DateTime(timezone=True), server_default=func.now())

    # Unique constraint already establishes a btree!
    __table_args__ = (UniqueConstraint('social_profile_id', 'social_profile_type', name='_social_profile_uc'),)


class Photo(base):
    __tablename__ = 'photo'

    id = Column(Integer, Sequence('photo_id_sequence', start=1, increment=1), primary_key=True)
    account_id = Column(Integer, ForeignKey('account.id'), nullable=False)
    photo_url = Column(String, nullable=False)
    creation_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    def to_dict(self):
        return {'id': self.id,
                'account_id': self.account_id,
                'photo_url': self.photo_url,
                'creation_time': int(self.creation_date.timestamp())}


# Sets up a sqlalchemy session
Session = sessionmaker(db)
session = Session()


# This allows you to run models.py to create the tables!
if __name__ == "__main__":
    base.metadata.create_all(db)