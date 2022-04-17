import sqlite3
from Packages.Users import *
"""
conn = sqlite3.connect('user.db')
with conn:
    user = ('addtest', 'addpasstest')
    Users.add_user(conn, user)
#
"""
Users.list_all()
#Users.remove_user('addtest')
    