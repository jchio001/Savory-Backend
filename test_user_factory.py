from models import FollowRelationship, User, session

import sys
import time


def create_test_user():
    user = User(social_profile_id=int(time.time()), social_profile_type='facebook',
                first_name='Jian', last_name='Yang',
                profile_image='https://i.kym-cdn.com/photos/images/newsfeed/001/130/355/dca.jpg')
    session.add(user)
    session.flush()
    session.commit()


def follow_user(follower_user_id, followed_user_id):
    if follower_user_id == followed_user_id:
        print('A user can\'t follow themselves!')
        return

    users = session \
        .query(User) \
        .filter(User.id.in_([follower_user_id, followed_user_id]))

    follower_user = None
    followed_user = None

    for user in users:
        if user.id == follower_user_id:
            follower_user = user
        elif user.id == followed_user_id:
            followed_user = user

    if not follower_user:
        print('Error: follower user does not exist.')
        return

    if not followed_user:
        print('Error: followed user does not exist')
        return

    follow_relationship = FollowRelationship(follower_user_id=follower_user_id,
                                             followed_user_id=followed_user_id)
    session.add(follow_relationship)
    session.commit()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Please specify an action.')
        sys.exit(1)

    action = sys.argv[1]
    if action == 'create':
        create_test_user()
    elif action == 'follow':
        follow_user(int(sys.argv[2]), int(sys.argv[3]))
