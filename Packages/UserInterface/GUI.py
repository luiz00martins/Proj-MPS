import sqlite3
import PySimpleGUI as sg
from ..Entities.Users import User, UserDefaultValidation
from ..DataStructures.Date import Date
from .Commands import Command, AddUserCommand, RemoveUserByUsernameCommand, CommandException


class GUI:
    __conn: sqlite3.Connection
    __prev_commands: list[Command]

    def __init__(self, conn: sqlite3.Connection):
        self.__conn = conn
        self.__prev_commands = []
        self.command_history = sg.Listbox([], size=(35, 8))

    def execute_command(self, command):
        try:
            command.execute()
            self.__prev_commands += [command]
            self.command_history.update([cm.get_name() for cm in self.__prev_commands])
        except CommandException:
            print('onho')

    def pop_command(self):
        if len(self.__prev_commands) > 0:
            last_command = self.__prev_commands.pop()
            last_command.undo()
            self.command_history.update([cm.get_name() for cm in self.__prev_commands])

    def run(self):

        # Define the window's contents
        layout = [[sg.Text("Username")],
                  [sg.Input(size=30, key='in_username'), sg.Text(key='err_username')],
                  [sg.Text("Password")],
                  [sg.Input(size=30, key='in_password'), sg.Text(key='err_password')],
                  [sg.Text("Birthday")],
                  [sg.Input(size=9, key='in_birthday_day'), sg.Input(size=9, key='in_birthday_month'),
                   sg.Input(size=9, key='in_birthday_year'), sg.Text(key='err_birthday')],
                  [sg.Text("Institute")],
                  [sg.Input(size=30, key='in_institute'), sg.Text(key='err_institute')],
                  [sg.Button('Add user'), sg.Button('Remove user from username'),
                   sg.Button('Undo')],
                  [self.command_history],
                  [sg.Button('Quit')]]

        # Create the window
        window = sg.Window('Window Title', layout)

        # Display and interact with the Window using an Event Loop
        while True:
            event, values = window.read()
            # See if user wants to quit or window was closed
            if event == sg.WINDOW_CLOSED or event == 'Quit':
                break
            elif event == 'Remove user from username':
                validation = UserDefaultValidation()
                command = RemoveUserByUsernameCommand(self.__conn, values['in_username'], validation)
                self.execute_command(command)

            elif event == 'Add user':
                user = User(values['in_username'], values['in_password'],
                            Date(int(values['in_birthday_day']), int(values['in_birthday_month']),
                                 int(values['in_birthday_year'])), values['in_institute'])
                validation = UserDefaultValidation()

                command = AddUserCommand(self.__conn, user, validation)
                self.execute_command(command)

                # Output a message to the window
                # window['err_username'].update(values['in_username'])
                # window['err_password'].update(values['in_password'])
                # window['err_birthday'].update(values['in_birthday'])
                # window['err_institute'].update(values['in_institute'])

            elif event == 'Undo':
                self.pop_command()

        # Finish up by removing from the screen
        window.close()
