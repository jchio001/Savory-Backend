import facebook_client
import logging
import savory_token_client

from models import Account, session
from sqlalchemy.exc import IntegrityError

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
            return savory_token_client.create_savory_token(account)
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

            return savory_token_client.create_savory_token(db_account)
    else:
        return facebook_client.create_facebook_error_response()