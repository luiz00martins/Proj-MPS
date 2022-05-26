from os import wait
import sqlite3
from Packages.Entities import Users, Institute, Classroom

from Packages.Entities.Classroom import Classroom, ClassroomRepository
from Packages.Entities.ClassroomUser import ClassroomUser, ClassroomUserRepository, Role

from Packages.DataStructures.Date import Date
from Packages.DataStructures.Treeset import TreeSet

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
    classroom_repo = ClassroomRepository(conn) 
    classroom_user_repo = ClassroomUserRepository(conn)

    # Clearing for testing

    for user in user_repo.get_all():
        user_repo.remove_user_by_id(user.id)

    for classroom in classroom_repo.get_all():
        classroom_repo.remove_classroom_by_code(classroom.code)

    for classroom_user in classroom_user_repo.get_all():
        classroom_user_repo.remove_classroom_user(classroom_user.user_fk, classroom_user.classroom_fk)

    # Tests

    user1 = Users.User('student', 'addpasstest22', Date(1,5,2015))
    user2 = Users.User('assistant', 'addpasstest22', Date(1,6,2010))
    user3 = Users.User('teacher', 'addpasstest22', Date(30,10,1999))
    user4 = Users.User('admin', 'addpasstest22', Date(5,7,2005))

    userError0 = Users.User('add1testa', 'addpasstest22', Date(2,6,1995))

    validation = Users.UserDefaultValidation()

    user_repo.add_user(user1, validation)
    user_repo.add_user(user2, validation)
    user_repo.add_user(user3, validation)
    user_repo.add_user(user4, validation)

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


    classroom_repo.add_classroom(Classroom("CS124"))

    for t in classroom_repo.get_all():
        print('\t', t)

    for t in classroom_repo.get_all():
        student = ClassroomUser(user1.id, t.code, Role.student)
        assistant = ClassroomUser(user2.id, t.code, Role.assistant)
        teacher = ClassroomUser(user3.id, t.code, Role.teacher)
        adiministrator = ClassroomUser(user4.id, t.code, Role.administrator)

        classroom_user_repo.add_classroom_user(student)
        classroom_user_repo.add_classroom_user(assistant)
        classroom_user_repo.add_classroom_user(teacher)
        classroom_user_repo.add_classroom_user(adiministrator)

        for cu in classroom_user_repo.get_all():
            print(f'User {cu.user_fk} is a {cu.role.name} in classroom {cu.classroom_fk}')

        classroom_user_repo.add_classroom_user(student)

