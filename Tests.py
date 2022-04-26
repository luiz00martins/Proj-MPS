import sqlite3
from Packages import Users

conn = sqlite3.connect('user.db')
with conn:
    user_repo = Users.UserRepository(conn)

    # Clearing for testing

    users = user_repo.get_all()

    for user in users:
        user_repo.remove_user_by_id(user.id)

    # Tests

    user1 = Users.User('addtest', 'addpasstest22')
    user2 = Users.User('addtesta', 'addpasstest22')
    user3 = Users.User('add1testa', 'addpasstest22')

    validation = Users.UserDefaultValidation()

    user_repo.add_user(user1, validation)
    user_repo.add_user(user2, validation)

    print('Print all: ')
    users = user_repo.get_all()
    for user in users:
        print('\t', user)

    print('Print by id, username: ')
    print('\t', user_repo.get_user_by_id(user1.id))
    print('\t', user_repo.get_user_by_username(user1.username))

    print('Print by id, username: ')
    print('\t', user_repo.get_user_by_id(user2.id))
    print('\t', user_repo.get_user_by_username(user2.username))

    print('Should be None: ', user_repo.get_user_by_username('ohno')) # Returns 'None'

    try:
        user_repo.add_user(user3, validation)
    except Users.UserValidationException as err:
        print(err)

    print('Print all: ')
    for user in users:
        print('\t', user)
    

