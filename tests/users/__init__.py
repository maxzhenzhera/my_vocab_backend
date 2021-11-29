from .user import TestUser


__all__ = [
    # types
    'TestUser',
    # instances
    'test_user_1',
    'test_user_2'
]


test_user_1 = TestUser('example1@gmail.com', 'password', 'google_id_1')
test_user_2 = TestUser('example2@gmail.com', 'password', 'google_id_2')
