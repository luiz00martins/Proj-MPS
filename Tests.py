from os import wait
import sqlite3
from Packages import Users, Institute, Classroom
from Packages.Date import Date
from Packages.Treeset import TreeSet

def init_db(conn: sqlite3.Connection):
    with open('db_definition.sql', 'r') as f:
        contents = f.read()
        cur = conn.cursor()
        cur.executescript(contents)
    
class UserComparer():
    def __init__(self, user):
        self.user = user

    def __str__(self):
        return str(self.user)

    def __lt__(self, other):
        return self.user.birthday < other.user.birthday
    def __eq__(self, other):
        return self.user.birthday == other.user.birthday
    def __gt__(self, other):
        return self.user.birthday > other.user.birthday
    def __ne__(self, other):
        return self.user.birthday != other.user.birthday
    def __le__(self, other):
        return self.user.birthday <= other.user.birthday
    def __ge__(self, other):
        return self.user.birthday >= other.user.birthday

def users_by_birthday_in_decreasing_order(users):
    return TreeSet([UserComparer(u) for u in users])

conn = sqlite3.connect('user.db')
with conn:
    init_db(conn)

    user_repo = Users.UserRepository(conn)

    # Clearing for testing

    users = user_repo.get_all()

    for user in users:
        user_repo.remove_user_by_id(user.id)

    # Tests

    user1 = Users.User('addtest', 'addpasstest22', Date(1,5,2015))
    user2 = Users.User('addtesta', 'addpasstest22', Date(1,6,2010))
    user3 = Users.User('addtestb', 'addpasstest22', Date(30,10,1999))

    userError0 = Users.User('add1testa', 'addpasstest22', Date(2,6,1995))

    validation = Users.UserDefaultValidation()

    user_repo.add_user(user1, validation)
    user_repo.add_user(user3, validation)
    user2_id = user_repo.add_user(user2, validation)

    print('Print all by birthday: ')
    users = user_repo.get_all()
    for user in users_by_birthday_in_decreasing_order(users):
        print('\t', user)

    print('Print by id, username: ')
    print('\t', user_repo.get_user_by_id(user1.id))
    print('\t', user_repo.get_user_by_username(user1.username))

    print('Print by id, username: ')
    print('\t', user_repo.get_user_by_id(user2.id))
    print('\t', user_repo.get_user_by_username(user2.username))

    print('Should be None: ', user_repo.get_user_by_username('ohno')) # Returns 'None'

    try:
        user_repo.add_user(userError0, validation)
    except Users.UserValidationException as err:
        print(err)

    userError1 = Users.User('usersab', 'passuserError02', Date(1, 10, 2001))
    user_repo.add_user(userError1, validation)

    print('Print all: ')
    users = user_repo.get_all()
    for user in users:
        print('\t', user)
    
    user_repo.remove_user_by_id(userError1.id)

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


    classroom_repo = Classroom.ClassroomRepository(conn) 

    classroom_repo.add_classroom(Classroom.Classroom("CS124"))

    for t in classroom_repo.get_all():
        print('\t', t)

    for t in classroom_repo.get_all():
        classroom_repo.remove_classroom_by_code(t.code)


# Testing dates and treeset.
ts = TreeSet([Date(1,5,2010),Date(1,5,2010),Date(2,5,2010),Date(2,5,2010),Date(1,5,1999)])
print(ts)

