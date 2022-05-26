import sqlite3

class Institute():
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return "Institute [name: {}]".format(self.name)

    def to_tuple(self):
        return (self.name,)

    @staticmethod
    def from_tuple(name: str):
        institute = Institute(name)
        return institute

class InsituteRepository:
    def __init__(self, conn: sqlite3.Connection):
        self.__conn = conn

    def __del__(self):
        self.__conn.close()

    def add_institute(self, institute: Institute):
        try:
            sql = '''
                INSERT INTO institute
                VALUES(?)
                '''

            cur = self.__conn.cursor()
            cur.execute(sql, institute.to_tuple())
            self.__conn.commit()
        except sqlite3.DatabaseError as err:
            print('Institute already exists in the database!'.upper())
            print('Error description: ', err)

    def get_institute(self, name: str) -> None | Institute:
        sql = f'''
            SELECT * FROM institute 
            WHERE name = ?
        '''
    
        cur = self.__conn.cursor()
        cur.execute(sql, (name,))
        res = cur.fetchone()

        if res == None:
            return None
        else:
            return Institute.from_tuple(*res)

    def remove_institute_by_name(self, name: str):
        try: 
            sql = f'''
                DELETE FROM institute 
                WHERE name = ?
            '''

            cur = self.__conn.cursor()
            cur.execute(sql, (name,))
            
            if(cur.rowcount == 0):
                print(f'Institute {name} does not exist')
                return

            print(f'Institute {name} successfully deleted')
            self.__conn.commit()
        except sqlite3.DataError as err:
            print(err.__traceback__)
    
    def get_all(self) -> list[Institute]:
        cursor = self.__conn.cursor()

        cursor.execute('''
        SELECT * FROM institute;  
        ''')

        result = cursor.fetchall()
        return [Institute.from_tuple(*t) for t in result]


