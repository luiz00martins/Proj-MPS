import json
import sqlite3

from Packages.DataExport.UserExporter import UserExporter


class JSONUserExporter(UserExporter):
    def __init__(self, conn: sqlite3.Connection):
        super().__init__(conn)

    def data_to_string(self) -> str:
        user_count = self.user_count()

        user_list = []
        for user in self.user_row():
            user_list.append({
                'id': str(user.id),
                'username': user.username,
                'birthday': user.birthday,
                'institute': user.institute_name
            })

        data = {
            "user_count": user_count,
            "users": user_list
        }

        return json.dumps(data, indent='  ')
