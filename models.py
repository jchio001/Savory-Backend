from sqlalchemy import BigInteger, create_engine, Column, DateTime, ForeignKey, Integer, Sequence, String, \
    UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func

import os

db_url = os.environ['SAVORY_DB_URL']
db = create_engine(db_url)
base = declarative_base()


class User(base):
    __tablename__ = 'user'

    id = Column(Integer, Sequence('user_id_seq', start=1, increment=1), primary_key=True)
    social_profile_id = Column(BigInteger, nullable=False)
    social_profile_type = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    profile_image = Column(String, nullable=False)
    creation_date = Column(DateTime(timezone=True), server_default=func.now())

    # Unique constraint already establishes a btree!
    __table_args__ = (UniqueConstraint('social_profile_id', 'social_profile_type', name='_social_profile_uc'),)

    def to_dict(self):
        return {'id': self.id,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'profile_image': self.profile_image,
                'creation_date': int(self.creation_date.timestamp())}


class Photo(base):
    __tablename__ = 'photos'

    id = Column(Integer, Sequence('photo_id_sequence', start=1, increment=1), primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, index=True)
    photo_url = Column(String, nullable=False)
    yelp_id = Column(String, nullable=False, index=True)
    # By attaching the name fetched from Yelp to the Photo object, we can avoid querying Yelp for information, which
    # makes the code simpler and faster!
    restaurant_name = Column(String, nullable=False)
    creation_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)

    def to_dict(self):
        return {'id': self.id,
                'user_id': self.user_id,
                'photo_url': self.photo_url,
                'yelp_id': self.yelp_id,
                'restaurant_name': self.restaurant_name,
                'creation_date': int(self.creation_date.timestamp())}


# Read this table as: User <follow_id> follows User <followed_user_id>
class FollowRelationship(base):
    __tablename__ = 'follow_relationship'

    follower_id = Column(Integer, ForeignKey('user.id'), nullable=False, index=True, primary_key=True)
    followed_user_id = Column(Integer, ForeignKey('user.id'), nullable=False, index=True, primary_key=True)

    follower_user = relationship(User,
                                 uselist=False,
                                 foreign_keys=[follower_id])
    followed_user = relationship(User,
                                 uselist=False,
                                 foreign_keys=[followed_user_id])


# Sets up a sqlalchemy session
Session = sessionmaker(db)
session = Session()


# This allows you to run models.py to create the tables!
if __name__ == "__main__":
    base.metadata.create_all(db)
