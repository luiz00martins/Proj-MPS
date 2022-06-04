import argparse
import sqlite3
from ..Entities.Users import UserRepository, User, UserDefaultValidation, UserValidationException

class UsersCLI():
    def __init__(self, conn: sqlite3.Connection):
        self.users = UserRepository(conn)

        self.parser = argparse.ArgumentParser(description='Manages users')

        self.parser.add_argument('--add', nargs=2, help='Adds a new user')
        self.parser.add_argument('--remove', nargs=1, help='Removes an existing user')
        self.parser.add_argument('--list', action='store_true', help='Prints all users')

    def _add(self):
        args = self.parser.parse_args()
        
        add_args = args.add
        
        # TODO: Add check if the user already exists.

        username = add_args[0]
        password = add_args[1]

        user = User(username, password)

        try:
            self.users.add_user(user, UserDefaultValidation())
        except UserValidationException as e:
            print("Falha ao adicionar usuario: " + e.reason)

    def _remove(self):
        args = self.parser.parse_args()
        
        add_args = args.remove
        
        # TODO: Add check if the user exists.

        username = add_args[0]

        self.users.remove_user_by_username(username)

    def _list(self):
        users_list = self.users.get_all()

        for usr in users_list:
            print(usr)

    def exec(self):
        args = self.parser.parse_args()

        if args.add is not None:
            self._add()
        if args.remove is not None:
            self._remove()
        if args.list:
            self._list()

