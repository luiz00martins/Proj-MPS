import sqlite3

def read_data():
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM users;  
    ''')

    for linha in cursor.fetchall():
        print(linha)
    conn.close()


read_data()

