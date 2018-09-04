import facebook_client
import logging
import photo_client
import savory_token_client

from models import User, Photo, session
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
            logging.warning('Account already exists in the system!')

            user = session \
                .query(User) \
                .filter_by(social_profile_id=facebook_account.id,
                           social_profile_type='facebook') \
                .first()

    return {'token': savory_token_client.create_savory_token(user)}, HTTP_STATUS_OK


def get_user(user_id):
    return session\
        .query(User)\
        .filter_by(id=user_id)\
        .first()


def get_user_info(user):
    return UserInfo(user=user,
                    photos_page=photo_client.get_stubbed_photos()).to_dict(), \
           HTTP_STATUS_OK


# TODO: Have this return the ids of all accounts being followed by the passed in account.
def get_following_accounts(user):
    return {user.id}


class UserInfo:

    def __init__(self, user, photos_page):
        self.user = user
        self.photos_page = photos_page

    def to_dict(self):
        return {'user': self.user.to_dict(),
                'photos': list(map(Photo.to_dict, self.photos_page))}
