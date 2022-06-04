from Packages.UserInterface.CLI import UsersCLI
from Packages.UserInterface.GUI import GUI
import sqlite3

GUI().run()

# def init_db(conn: sqlite3.Connection):
#     with open('db_definition.sql', 'r') as f:
#         contents = f.read()
#         cur = conn.cursor()
#         cur.executescript(contents)
# 
# conn = sqlite3.connect('user.db')
# 
# init_db(conn)
# 
# cli = UsersCLI(conn)
# cli.exec()
