import sqlite3


class User():
    def __init__(self, username, password):
        if len(username) == 0:
            raise ValueError('No username provided')
        if len(username) > 12:
            raise ValueError('Username is too long')
        if not any(c.isdigit() for c in username):
            raise ValueError('Username contains numbers')

        if len(password) >= 20:
            raise ValueError('Password is too long')
        if len(password) <= 8:
            raise ValueError('Password is too long')
        if len([x for x in password if x.isdigit()]) < 2:
            raise ValueError('Password must have at least 2 numbers')

        self.username = username
        self.password = password

class Users():
    def __init__(self):
        # TODO:
        pass

    def add_user(conn, user):
        sql = '''
            INSERT INTO users(username, password)
            VALUES(?,?)
        '''
        cur = conn.cursor()
        cur.execute(sql, user)
        conn.commit()
        return cur.lastrowid

    def remove_user(username):
        conn = sqlite3.connect('user.db')
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM users
            WHERE username = ?
        
        ''', [username])
        print(f'Usuário {username} deletado com sucesso')
        conn.commit()
        conn.close()

    def list_all():
        conn = sqlite3.connect('user.db')
        cursor = conn.cursor()

        cursor.execute('''
        SELECT * FROM users;  
        ''')

        for linha in cursor.fetchall():
            print(linha)
        conn.close()

