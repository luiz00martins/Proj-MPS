import sqlite3
from abc import abstractmethod
from enum import Enum, auto

from .Users import User
from ..DataStructures.Date import Date


class DatabaseError(Exception):
    pass


class Role(Enum):
    student = auto()
    assistant = auto()
    teacher = auto()
    administrator = auto()


# FIXME: This is a horrible name.
class ClassroomUserRole:
    def __init__(self, user_fk: int, classroom_fk: str, role: Role):
        self.user_fk = user_fk
        self.classroom_fk = classroom_fk
        self.role = role

    def to_tuple(self):
        return self.user_fk, self.classroom_fk, self.role.name

    @staticmethod
    def from_tuple(user: int, classroom: str, role: Role):
        return ClassroomUserRole(user, classroom, role)


class ClassroomUserRoleRepository:
    # TODO: Create the template pattern with this and the Classroom.py/User.py.

    def __init__(self, conn: sqlite3.Connection):
        self.__conn = conn

    def __del__(self):
        self.__conn.close()

    def add_classroom_user(self, classroom_user: ClassroomUserRole):
        try:
            sql = '''
                INSERT INTO classroom_user(user_fk, classroom_fk, role)
                VALUES(?, ?, ?)
                '''

            cur = self.__conn.cursor()
            cur.execute(sql, classroom_user.to_tuple())
            self.__conn.commit()
        except sqlite3.DatabaseError as err:
            print(f'User {classroom_user.user_fk} is already in classroom {classroom_user.classroom_fk}')
            print('Error description: ', err)

    def get_classroom(self, user_fk: int, classroom_fk: str, role: Role) -> None | ClassroomUserRole:
        sql = f'''
            SELECT * FROM classroom_user
            WHERE user_fk = ? AND classroom_fk = ? AND role = ?
        '''

        cur = self.__conn.cursor()
        cur.execute(sql, (user_fk, classroom_fk, role.name))
        res = cur.fetchone()

        if res is None:
            return None
        else:
            return ClassroomUserRole.from_tuple(*res)

    def remove_classroom_user(self, user_fk: int, classroom_fk: str):
        try:
            sql = f'''
                DELETE FROM classroom_user
                WHERE user_fk = ? AND classroom_fk = ?
            '''

            cur = self.__conn.cursor()
            cur.execute(sql, (user_fk, classroom_fk))

            if cur.rowcount == 0:
                print(f'User {user_fk} is not in classroom {classroom_fk}')
                return

            print(f'User {user_fk} successfully deleted from classroom {classroom_fk}')
            self.__conn.commit()
        except sqlite3.DataError as err:
            print(err.__traceback__)

    def get_all(self) -> list[ClassroomUserRole]:
        cursor = self.__conn.cursor()

        cursor.execute('''
        SELECT user_fk, classroom_fk, role
        FROM classroom_user;  
        ''')

        result = cursor.fetchall()

        return [ClassroomUserRole.from_tuple(user_fk, classroom_fk, Role[role_name]) for
                user_fk, classroom_fk, role_name in result]


class ClassroomUser(User):
    def __init__(self, username: str, password: str, birthday: Date, classroom_fk: str, role: Role):
        User.__init__(self, username, password, birthday)
        self.classroom_fk = classroom_fk
        self.role = role

    @abstractmethod
    def get_credentials(self):
        pass

    @abstractmethod
    def clone(self):
        pass


class Student(ClassroomUser):
    def get_credentials(self):
        print(
            f'I, {self.username}, am allowed to watch classes, participate in them, and see my statistics in the '
            f'class in classroom {self.classroom_fk}.')

    def clone(self):
        return Student(self.username, self.password, self.birthday, self.classroom_fk, self.role)


class Assistant(ClassroomUser):
    def get_credentials(self):
        print(
            f'I, {self.username}, am allowed to participate in classes, present them, and moderate them in classroom '
            f'{self.classroom_fk}.')

    def clone(self):
        return Student(self.username, self.password, self.birthday, self.classroom_fk, self.role)


class Teacher(ClassroomUser):
    def get_credentials(self):
        print(
            f'I, {self.username}, am allowed to create classes, present them, and moderate them. Furthermore, '
            f'I can access all of the student\'s statistics, and grade students in classroom {self.classroom_fk}.')

    def clone(self):
        return Student(self.username, self.password, self.birthday, self.classroom_fk, self.role)


class Administrator(ClassroomUser):
    def get_credentials(self):
        print(
            f'I, {self.username}, am allowed to create classes, and moderate them in classroom {self.classroom_fk}. '
            f'Furthermore, I can access all of the student\'s statistics, post messages to the classroom\'s board, '
            f'and send alerts in the classroom\'s board')

    def clone(self):
        return Student(self.username, self.password, self.birthday, self.classroom_fk, self.role)


def create_classroom_user(cls_usr_role: ClassroomUserRole, conn: sqlite3.Connection) -> ClassroomUser:
    sql = f'''
        SELECT username, password, birthday FROM users
        WHERE id = ?
    '''

    cur = conn.cursor()
    cur.execute(sql, [cls_usr_role.user_fk])
    res = cur.fetchone()

    if res is None:
        raise DatabaseError(f'User {cls_usr_role.user_fk} does not exist in the database')

    args = (res[0], res[1], res[2], cls_usr_role.classroom_fk, cls_usr_role.role)
    match cls_usr_role.role.name:
        case 'student':
            return Student(*args)
        case 'assistant':
            return Assistant(*args)
        case 'teacher':
            return Teacher(*args)
        case 'administrator':
            return Administrator(*args)

    raise ValueError(f'No role of type {cls_usr_role.role.name}')
