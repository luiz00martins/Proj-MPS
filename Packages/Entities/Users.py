import sqlite3
from ..DataStructures.Date import Date

class User():
    def __init__(self, username: str, password: str, birthday: Date, institute_name: str = None):
        self.username = username
        self.password = password
        self.birthday = birthday
        self.id = 0
        self.institute_name = institute_name

    def __str__(self):
        return f"User [id: {self.id}; username: {self.username}; birthday: {self.birthday}; password: {self.password}]"

    def to_tuple(self):
        return (self.username, self.password, str(self.birthday), self.institute_name)

    @staticmethod
    def from_tuple(id: int, username: str, password: str, birthday: Date, institute_fk: int):
        user = User(username, password, birthday)
        user.id = id
        user.institute_name = institute_fk
        return user

class UserValidationException(Exception):
    def __init__(self, reason):
        self.reason = reason

    def __str__(self):
        return f"user validation failed, reason: {self.reason}"


class UserDefaultValidation():

    def validate(self, user: User):
        if len(user.username) == 0:
            raise UserValidationException('No username provided')
        if len(user.username) > 12:
            raise UserValidationException('Username is too long')
        if any([c.isdigit() for c in user.username]):
            raise UserValidationException('Username contains numbers')

        if len(user.password) >= 20:
            raise UserValidationException('Password is too long')
        if len(user.password) <= 8:
            raise UserValidationException('Password is too short')
        if len([x for x in user.password if x.isdigit()]) < 2:
            raise UserValidationException('Password must have at least 2 numbers')


class UserRepository:
    def __init__(self, conn: sqlite3.Connection):
        self.__conn = conn

    # def __del__(self):
    #     self.__conn.close()

    def add_user(self, user: User, validation) -> int:
        # TODO: check if user already exists before trying to insert
        try:
            sql = '''
                INSERT INTO users(username, password, birthday, institute_fk)
                VALUES(?,?,?,?)
                '''

            validation.validate(user)
            cur = self.__conn.cursor()
            cur.execute(sql, user.to_tuple())
            self.__conn.commit()
            id = cur.lastrowid
            user.id = id
            return id
        except sqlite3.DatabaseError as err:
            print('Username already exists in the database'.upper())
            print('Error description: ', err)

    def __get_user_helper(self, parameter, argument):
        sql = f'''
            SELECT * FROM users
            WHERE {parameter} = ?
        '''
    
        cur = self.__conn.cursor()
        cur.execute(sql, [argument])
        res = cur.fetchone()


        if res == None:
            return None
        else:
            return User.from_tuple(*res)

    def get_user_by_id(self, id: int) -> User | None:
        return self.__get_user_helper('id', id)

    def get_user_by_username(self, username: str) -> User | None:
        return self.__get_user_helper('username', username)

    def __remove_user_helper(self, parameter, argument):
        try: 
            sql = f'''
                DELETE FROM users
                WHERE {parameter} = ?
            '''

            cur = self.__conn.cursor()
            cur.execute(sql, [argument])
            
            if(cur.rowcount == 0):
                print(f'User {argument} does not exist')
                return

            print(f'User with {parameter}: {argument} successfully deleted')
            self.__conn.commit()
        except sqlite3.DataError as err:
            print(err.__traceback__)

    def remove_user_by_id(self, id: int):
        return self.__remove_user_helper('id', id)

    def remove_user_by_username(self, username: str):
        return self.__remove_user_helper('username', username)

    def get_all(self) -> list[User]:
        cursor = self.__conn.cursor()

        cursor.execute('''
        SELECT * FROM users;  
        ''')

        result = cursor.fetchall()
        return [User.from_tuple(*t) for t in result]



