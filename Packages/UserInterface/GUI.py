import sqlite3
import PySimpleGUI as sg
from ..Entities.Users import User, UserRepository, UserDefaultValidation
from ..DataStructures.Date import Date
from .Commands import AddUserCommand, RemoveUserByUsernameCommand 


class GUI():
    def __init__(self, conn: sqlite3.Connection):
        self.__conn = conn

    def run(self):
        # Define the window's contents
        layout = [[sg.Text("Username")],
                  [sg.Input(size = 30, key='in_username'), sg.Text(key='err_username')],
                  [sg.Text("Password")],
                  [sg.Input(size = 30, key='in_password'), sg.Text(key='err_password')],
                  [sg.Text("Birthday")],
                  [sg.Input(size = 9, key='in_birthday_day'), sg.Input(size = 9, key='in_birthday_month'), sg.Input(size = 9, key='in_birthday_year'), sg.Text(key='err_birthday')],
                  [sg.Text("Institute")],
                  [sg.Input(size = 30, key='in_institute'), sg.Text(key='err_institute')],
                  [sg.Button('Add user'), sg.Button('Remove user from username'), sg.Button('Quit')]]

        # Create the window
        window = sg.Window('Window Title', layout)

        # Display and interact with the Window using an Event Loop
        while True:
            event, values = window.read()
            # See if user wants to quit or window was closed
            if event == sg.WINDOW_CLOSED or event == 'Quit':
                break
            elif event == 'Remove user from username':
                command = RemoveUserByUsernameCommand(self.__conn, (values['in_username'],))
                command.execute()

            elif event == 'Add user':
                user = User(values['in_username'], values['in_password'], Date(int(values['in_birthday_day']), int(values['in_birthday_month']), int(values['in_birthday_year'])), values['in_institute'])
                validation = UserDefaultValidation()

                command = AddUserCommand(self.__conn, (user, validation))
                command.execute()

                # Output a message to the window
                # window['err_username'].update(values['in_username'])
                # window['err_password'].update(values['in_password'])
                # window['err_birthday'].update(values['in_birthday'])
                # window['err_institute'].update(values['in_institute'])

        # Finish up by removing from the screen
        window.close()
