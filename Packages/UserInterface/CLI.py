import argparse
import sqlite3
from ..Entities.Users import UserRepository, User, UserDefaultValidation, UserValidationException
from ..DataStructures.Date import Date
from .Commands import AddUserCommand, RemoveUserByUsernameCommand, GetAllUsersCommand 

class UsersCLI():
    def __init__(self, conn: sqlite3.Connection):
        self.__conn = conn

        self.parser = argparse.ArgumentParser(description='Manages users')

        self.parser.add_argument('--add', nargs=4, help='Adds a new user')
        self.parser.add_argument('--remove', nargs=1, help='Removes an existing user')
        self.parser.add_argument('--list', action='store_true', help='Prints all users')

    def _add(self):
        args = self.parser.parse_args()
        
        add_args = args.add
        
        # TODO: Add check if the user already exists.

        username = add_args[0]
        password = add_args[1]
        birthday = add_args[2]
        institute = add_args[3]

        birthday = [int(v) for v in birthday.split('/')]
        birthday = Date(birthday[0], birthday[1], birthday[2])
        
        user = User(username, password, birthday, institute)
        validation = UserDefaultValidation()

        try:
            command = AddUserCommand(self.__conn, (user, validation))
            command.execute()
        except UserValidationException as e:
            print("Falha ao adicionar usuario: " + e.reason)

    def _remove(self):
        args = self.parser.parse_args()
        
        add_args = args.remove
        
        # TODO: Add check if the user exists.

        username = add_args[0]

        command = RemoveUserByUsernameCommand(self.__conn, (username,))
        command.execute()

    def _list(self):
        command = GetAllUsersCommand(self.__conn, ())
        users_list = command.execute()

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

