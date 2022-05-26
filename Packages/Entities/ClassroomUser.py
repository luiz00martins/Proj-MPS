import sqlite3
from enum import Enum, auto

from .Users import User, UserRepository
from .Classroom import Classroom, ClassroomRepository

class Role(Enum):
    student = auto()
    assistant = auto()
    teacher = auto()
    administrator = auto()

class ClassroomUser():
    def __init__(self, user_fk: int, classroom_fk: str, role: Role):
        self.user_fk = user_fk
        self.classroom_fk = classroom_fk
        self.role = role

    def to_tuple(self):
        return (self.user_fk, self.classroom_fk, self.role.name)

    @staticmethod
    def from_tuple(user: int, classroom: str, role: Role):
        return ClassroomUser(user, classroom, role)
        

        
class ClassroomUserRepository:
    # TODO: Create the template pattern with this and the Classroom.py/User.py.

    def __init__(self, conn: sqlite3.Connection):
        self.__conn = conn

    def __del__(self):
        self.__conn.close()

    def add_classroom_user(self, classroom_user: ClassroomUser):
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

    def get_classroom(self, user_fk: int, classroom_fk: str, role: Role) -> None | ClassroomUser:
        sql = f'''
            SELECT * FROM classroom_user
            WHERE user_fk = ? AND classroom_fk = ? AND role = ?
        '''

        cur = self.__conn.cursor()
        cur.execute(sql, (user_fk, classroom_fk, role.name))
        res = cur.fetchone()

        if res == None:
            return None
        else:
            return ClassroomUser.from_tuple(*res)

    def remove_classroom_user(self, user_fk: int, classrooml_fk: str):
        try: 
            sql = f'''
                DELETE FROM classroom_user
                WHERE user_fk = ? AND classroom_fk = ?
            '''

            cur = self.__conn.cursor()
            cur.execute(sql, (user_fk, classrooml_fk))
            
            if(cur.rowcount == 0):
                print(f'User {user_fk} is not in classroom {classrooml_fk}')
                return

            print(f'User {user_fk} successfully deleted from classroom {classrooml_fk}')
            self.__conn.commit()
        except sqlite3.DataError as err:
            print(err.__traceback__)
    
    def get_all(self) -> list[ClassroomUser]:
        cursor = self.__conn.cursor()

        cursor.execute('''
        SELECT user_fk, classroom_fk, role
        FROM classroom_user;  
        ''')

        result = cursor.fetchall()

        return [ClassroomUser.from_tuple(user_fk, classroom_fk, Role[role_name]) for user_fk, classroom_fk, role_name in result]


