import facebook_client
import logging
import photo_client
import savory_token_client

from models import Account, Photo, session
from sqlalchemy.exc import IntegrityError
from status_codes import HTTP_STATUS_OK


def create_or_update_existing_profile(facebook_account):
    account = Account(social_profile_id=facebook_account.id, social_profile_type='facebook',
                      first_name=facebook_account.first_name, last_name=facebook_account.last_name,
                      profile_image=facebook_account.profile_image)

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
