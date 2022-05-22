import sqlite3

class Turma():
    def __init__(self, code: str):
        self.code = code

    def __str__(self):
        out_str = "Turma [code: {}]"
        return out_str.format(self.code)

    def to_tuple(self):
        return (self.code,)

    @staticmethod
    def from_tuple(code: str):
        turma = Turma(code)
        return turma


class TurmaRepository:
    def __init__(self, conn: sqlite3.Connection):
        self.__conn = conn

    def __del__(self):
        self.__conn.close()

    def add_turma(self, turma: Turma):
        try:
            sql = '''
                INSERT INTO turma(code)
                VALUES(?)
                '''

            cur = self.__conn.cursor()
            cur.execute(sql, turma.to_tuple())
            self.__conn.commit()
        except sqlite3.DatabaseError as err:
            print('A turma digitada ja existe em nosso banco de dados!'.upper())
            print('Error description: ', err)

    def get_turma(self, code: str) -> None | Turma:
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
            return Turma.from_tuple(*res)

    def remove_turma_by_code(self, code: str):
        try: 
            sql = f'''
                DELETE FROM turma
                WHERE code = ?
            '''

            cur = self.__conn.cursor()
            cur.execute(sql, [code])
            
            if(cur.rowcount == 0):
                print(f'Turma {code} nao existe')
                return

            print(f'Turma {code} deletado com sucesso')
            self.__conn.commit()
        except sqlite3.DataError as err:
            print(err.__traceback__)
    
    def get_all(self) -> list[Turma]:
        cursor = self.__conn.cursor()

        cursor.execute('''
        SELECT * FROM turma;  
        ''')

        result = cursor.fetchall()
        return [Turma.from_tuple(*t) for t in result]

