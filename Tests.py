from os import wait
import sqlite3
from Packages import Users, Institute, Turma, Treeset, Date

# Testing database.
def init_db(conn: sqlite3.Connection):
    with open('db_definition.sql', 'r') as f:
        contents = f.read()
        cur = conn.cursor()
        cur.executescript(contents)
    

conn = sqlite3.connect('user.db')
with conn:
    init_db(conn)

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
    user2_id = user_repo.add_user(user2, validation)

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

    user4 = Users.User('usersab', 'passuser32')
    user_repo.add_user(user4, validation)

    print('Print all: ')
    users = user_repo.get_all()
    for user in users:
        print('\t', user)
    
    user_repo.remove_user_by_id(user4.id)

    print('Print all: ')
    users = user_repo.get_all()
    for user in users:
        print('\t', user)

    institute_repo = Institute.InsituteRepository(conn)

    institute_repo.add_institute(Institute.Institute("UFPB"))

    for i in institute_repo.get_all():
        print('\t', i)

    ufpb = institute_repo.get_institute("UFPB")
    print('\t', ufpb)

    for i in institute_repo.get_all():
        institute_repo.remove_institute_by_name(i.name)


    turma_repo = Turma.TurmaRepository(conn) 

    turma_repo.add_turma(Turma.Turma("CS124"))

    for t in turma_repo.get_all():
        print('\t', t)

    for t in turma_repo.get_all():
        turma_repo.remove_turma_by_code(t.code)


# Testing dates and treeset.
Date = Date.Date
ts = Treeset.TreeSet([Date(1,5,2010),Date(1,5,2010),Date(2,5,2010),Date(2,5,2010),Date(1,5,1999)])
print(ts)

