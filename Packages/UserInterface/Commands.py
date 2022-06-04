import sqlite3
from ..Entities.Users import User, UserDefaultValidation, UserRepository

class Command():
    def __init__(self, conn, args: tuple):
        self.repo = UserRepository(conn)
        self.args = args


class AddUserCommand(Command):

    def execute(self):
        return self.repo.add_user(*self.args)

class RemoveUserByUsernameCommand(Command):
    
    def execute(self):
        return self.repo.remove_user_by_username(*self.args)

class GetAllUsersCommand(Command):
    
    def execute(self):
        return self.repo.get_all(*self.args)
