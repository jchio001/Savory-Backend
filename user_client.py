import logging
import photo_client
import savory_token_client

from models import FollowRelationship, User, Photo, session
from sqlalchemy.exc import IntegrityError
from status_codes import HTTP_STATUS_OK


def create_or_update_existing_account(facebook_account):
    user = session \
        .query(User) \
        .filter_by(social_profile_id=facebook_account.id,
                   social_profile_type='facebook') \
        .first()

    if not user:
        try:
            user = User(social_profile_id=facebook_account.id, social_profile_type='facebook',
                        first_name=facebook_account.first_name, last_name=facebook_account.last_name,
                        profile_image=facebook_account.profile_image)
            session.add(user)
            session.flush()
            session.commit()
        except IntegrityError:
            session.rollback()
            logging.warning('User already exists in the system!')

            user = session \
                .query(User) \
                .filter_by(social_profile_id=facebook_account.id,
                           social_profile_type='facebook') \
                .first()

    return {'token': savory_token_client.create_savory_token(user)}, HTTP_STATUS_OK


def get_user(user_id):
    return session \
        .query(User) \
        .filter_by(id=user_id) \
        .first()


def get_user_info(user):
    return UserInfo(user=user,
                    photos_page=photo_client.get_stubbed_photos()).to_dict(), \
           HTTP_STATUS_OK


# Following as in the users this user follows
def get_followed_user_ids_for_user(user):
    return session \
        .query(FollowRelationship.followed_user_id) \
        .filter_by(follower_user_id=user.id) \
        .all()


# Given a user, gets the users that they are following.
def get_followed_users_for_user(user):
    following_relationships = session \
        .query(FollowRelationship) \
        .join(User, User.id == FollowRelationship.followed_user_id) \
        .filter(FollowRelationship.follower_user_id == user.id) \
        .all()
    return list(map(lambda f: f.followed_user.to_dict(), following_relationships)), HTTP_STATUS_OK


class UserInfo:

    def __init__(self, user, photos_page):
        self.user = user
        self.photos_page = photos_page

    def to_dict(self):
        return {'user': self.user.to_dict(),
                'photos': list(map(Photo.to_dict, self.photos_page))}
