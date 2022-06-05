import sqlite3
from abc import abstractmethod

from ..Entities.Users import User, UserDefaultValidation, UserRepository, UserRepoException


class CommandException(Exception):
    def __init__(self):
        super().__init__()


class Command:
    def __init__(self, conn):
        self.repo = UserRepository(conn)

    @abstractmethod
    def undo(self):
        pass

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass


class AddUserCommand(Command):
    def __init__(self, conn: sqlite3.Connection, user: User, validation: UserDefaultValidation):
        super().__init__(conn)
        self.__user = user
        self.__validation = validation

    def undo(self):
        self.repo.remove_user_by_id(self.__user.id)

    def execute(self):
        try:
            self.repo.add_user(self.__user, self.__validation)
        except UserRepoException:
            raise CommandException

    def get_name(self) -> str:
        return 'Add User'


class RemoveUserByUsernameCommand(Command):
    def __init__(self, conn: sqlite3.Connection, username: str, validation: UserDefaultValidation):
        super().__init__(conn)
        self.__username = username
        self.__validation = validation
        self.__user = None

    def undo(self):
        self.repo.add_user(self.__user, self.__validation)

    def execute(self):
        self.__user = self.repo.get_user_by_username(self.__username)
        self.repo.remove_user_by_username(self.__user.username)

    def get_name(self) -> str:
        return 'Remove User'


# TODO: Not useful as a command?
class GetAllUsersCommand(Command):
    def __init__(self, conn: sqlite3.Connection):
        super().__init__(conn)

    def undo(self):
        return None

    def execute(self):
        self.repo.get_all()
