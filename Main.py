from Packages.CLI import UsersCLI
import sqlite3

conn = sqlite3.connect('user.db')

cli = UsersCLI(conn)

cli.exec()
