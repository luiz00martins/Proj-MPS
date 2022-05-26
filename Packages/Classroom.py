import sqlite3

class Classroom():
    def __init__(self, code: str):
        self.code = code

    def __str__(self):
        out_str = "Classroom [code: {}]"
        return out_str.format(self.code)

    def to_tuple(self):
        return (self.code,)

    @staticmethod
    def from_tuple(code: str):
        classroom = Classroom(code)
        return classroom


class ClassroomRepository:
    def __init__(self, conn: sqlite3.Connection):
        self.__conn = conn

    def __del__(self):
        self.__conn.close()

    def add_classroom(self, classroom: Classroom):
        try:
            sql = '''
                INSERT INTO classroom(code)
                VALUES(?)
                '''

            cur = self.__conn.cursor()
            cur.execute(sql, classroom.to_tuple())
            self.__conn.commit()
        except sqlite3.DatabaseError as err:
            print('A classroom digitada ja existe em nosso banco de dados!'.upper())
            print('Error description: ', err)

    def get_classroom(self, code: str) -> None | Classroom:
        sql = f'''
            SELECT * FROM users
            WHERE code = ?
        '''
    
        cur = self.__conn.cursor()
        cur.execute(sql, code)
        res = cur.fetchone()

        if res == None:
            return None
        else:
            return Classroom.from_tuple(*res)

    def remove_classroom_by_code(self, code: str):
        try: 
            sql = f'''
                DELETE FROM classroom
                WHERE code = ?
            '''

            cur = self.__conn.cursor()
            cur.execute(sql, [code])
            
            if(cur.rowcount == 0):
                print(f'Classroom {code} nao existe')
                return

            print(f'Classroom {code} deletado com sucesso')
            self.__conn.commit()
        except sqlite3.DataError as err:
            print(err.__traceback__)
    
    def get_all(self) -> list[Classroom]:
        cursor = self.__conn.cursor()

        cursor.execute('''
        SELECT * FROM classroom;  
        ''')

        result = cursor.fetchall()
        return [Classroom.from_tuple(*t) for t in result]

