import facebook_client
import logging
import photo_client
import savory_token_client

from models import Account, Photo, session
from sqlalchemy.exc import IntegrityError
from status_codes import HTTP_STATUS_OK


def create_or_update_existing_account(facebook_account):
    account = session \
        .query(Account) \
        .filter_by(social_profile_id=facebook_account.id,
                   social_profile_type='facebook') \
        .first()

    if not account:
        try:
            account = Account(social_profile_id=facebook_account.id, social_profile_type='facebook',
                              first_name=facebook_account.first_name, last_name=facebook_account.last_name,
                              profile_image=facebook_account.profile_image)
            session.add(account)
            session.flush()
            session.commit()
        except IntegrityError:
            session.rollback()
            logging.warning('Account already exists in the system!')

            account = session \
                .query(Account) \
                .filter_by(social_profile_id=facebook_account.id,
                           social_profile_type='facebook') \
                .first()

    return {'token': savory_token_client.create_savory_token(account)}, HTTP_STATUS_OK


def get_account(account_id):
    return session\
        .query(Account)\
        .filter_by(id=account_id)\
        .first()


def get_account_info(account):
    return AccountInfo(account=account,
                       photos_page=photo_client.get_photos_page_for_account()).to_dict(), \
           HTTP_STATUS_OK


class AccountInfo:

    def __init__(self, account, photos_page):
        self.account = account
        self.photos_page = photos_page

    def to_dict(self):
        return {'account': self.account.to_dict(),
                'photos': list(map(Photo.to_dict, self.photos_page))}
