from Packages.UserInterface.CLI import UsersCLI
from Packages.UserInterface.GUI import GUI
import sqlite3


def init_db(conn: sqlite3.Connection):
    with open('db_definition.sql', 'r') as f:
        contents = f.read()
        cur = conn.cursor()
        cur.executescript(contents)


with sqlite3.connect('test.db') as conn:
    init_db(conn)
    GUI(conn).run()

# 
# conn = sqlite3.connect('user.db')
# 
# init_db(conn)
# 
# cli = UsersCLI(conn)
# cli.exec()
