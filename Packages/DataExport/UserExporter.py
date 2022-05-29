import sqlite3
from abc import abstractmethod
from Packages.Entities.Users import User, UserRepository


class UserExporter:
    def __init__(self, conn: sqlite3.Connection):
        self.__conn = conn
        self.__users = UserRepository(conn).get_all()

    def user_count(self) -> int:
        return len(self.__users)

    def user_row(self) -> list[User]:
        return self.__users

    @abstractmethod
    def data_to_string(self) -> str:
        pass

    def export_data(self, filename: str):
        output_str = self.data_to_string()

        with open(filename, 'w') as file:
            file.write(output_str)

    def debug(self):
        print(self.__user_count())
        print(self.__user_row())
