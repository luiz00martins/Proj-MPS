import PySimpleGUI as sg

class GUI():
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
                  [sg.Button('Ok'), sg.Button('Quit')]]

        # Create the window
        window = sg.Window('Window Title', layout)

        # Display and interact with the Window using an Event Loop
        while True:
            event, values = window.read()
            # See if user wants to quit or window was closed
            if event == sg.WINDOW_CLOSED or event == 'Quit':
                break
            elif event == 'Ok':
                # Output a message to the window
                window['err_username'].update(values['in_username'])
                window['err_password'].update(values['in_password'])
                window['err_birthday'].update(values['in_birthday'])
                window['err_institute'].update(values['in_institute'])

        # Finish up by removing from the screen
        window.close()
