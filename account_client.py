import facebook_client
import logging
import photo_client
import savory_token_client

from models import Account, Photo, session
from sqlalchemy.exc import IntegrityError
from status_codes import HTTP_STATUS_OK


def create_or_update_existing_profile(social_profile_token):
    fb_profile_response = facebook_client.get_profile(social_profile_token)

    if fb_profile_response.is_successful():
        fb_profile = fb_profile_response.response_dict
        account = Account(social_profile_id=fb_profile['id'], social_profile_type='facebook',
                          first_name=fb_profile['first_name'], last_name=fb_profile['last_name'],
                          profile_image=fb_profile['picture']['data']['url'])

        try:
            session.add(account)
            session.flush()
            session.commit()
            return {'token': savory_token_client.create_savory_token(account)}, HTTP_STATUS_OK
        except IntegrityError:
            session.rollback()
            logging.warning('Account already exists in the system!')

            db_account = session \
                .query(Account) \
                .filter_by(social_profile_id=account.social_profile_id,
                           social_profile_type=account.social_profile_type) \
                .first()

            db_account.first_name = account.first_name
            db_account.last_name = account.last_name
            db_account.profile_image = account.profile_image

            session.commit()

            logging.info('Updated account!')
            
            return {'token': savory_token_client.create_savory_token(db_account)}, HTTP_STATUS_OK
    else:
        return facebook_client.create_facebook_error_response()


def get_account(account_id):
    return session\
        .query(Account)\
        .filter_by(id=account_id)\
        .first()


def get_account_info(account):
    return AccountInfo(account=account, photo_page=photo_client.get_photos()).to_dict(), HTTP_STATUS_OK


class AccountInfo:

    def __init__(self, account, photo_page):
        self.account = account
        self.photo_page = photo_page

    def to_dict(self):
        return {'account': self.account.to_dict(),
                'photos': list(map(Photo.to_dict, self.photo_page))}
