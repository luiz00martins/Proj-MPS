import sqlite3

import xml.etree.ElementTree as ElTree

from Packages.DataExport.UserExporter import UserExporter


class XMLUserExporter(UserExporter):
    def __init__(self, conn: sqlite3.Connection):
        super().__init__(conn)

    def data_to_string(self) -> str:
        data = ElTree.Element('UserData')
        ElTree.SubElement(data, 'UserCount').text = str(self.user_count())

        users = ElTree.SubElement(data, 'Users')

        for user in self.user_row():
            user_el = ElTree.SubElement(users, 'User')

            ElTree.SubElement(user_el, 'UserId').text = str(user.id)
            ElTree.SubElement(user_el, 'UserName').text = user.username
            ElTree.SubElement(user_el, 'Birthday').text = user.birthday
            ElTree.SubElement(user_el, 'Institute').text = user.institute_name

        return ElTree.tostring(data, encoding='unicode')