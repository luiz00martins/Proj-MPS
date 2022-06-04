import sqlite3

from .Entities.Users import User, UserRepository, UserDefaultValidation
from .DataStructures.Date import Date

class PdfAdapter():
    def __init__(self, conn: sqlite3.Connection):
        self.repo = UserRepository(conn)

    def _convert_pdf(self, text):
        print("Splitting string... ", end="")
        print("Converting to list of dicts... ", end="")

        converted = [
                User('pdf_user_a', '123456789', Date(1,1,2000), 'outside_institute'),
                User('pdf_user_b', '123456789', Date(1,1,2000), 'outside_institute'),
                User('pdf_user_c', '123456789', Date(1,1,2000), 'outside_institute'),
                ]

        return converted

    # Converts a pdf file with a table to a format that can be saved to the database, and stores it.
    def import_pdf(self, path: str):
        print(f"[PdfAdapter] Opening file {path}... ", end="")
        print("Reading as string... ", end="")
        input = 'some text'

        print("Converting to proper format... ", end="")
        lst = self._convert_pdf(input)

        print("Storing data... ", end="")
        for user in lst:
            print(f"Adding user {user.username}, ", end="")
            self.repo.add_user(user, UserDefaultValidation())
        print("Done.")

        return

        
        

