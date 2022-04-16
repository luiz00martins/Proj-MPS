
class User():
    def __init__(self, username, password):
        if len(username) == 0:
            raise ValueError('No username provided')
        if len(username) > 12:
            raise ValueError('Username is too long')
        if not any(c.isdigit() for c in username):
            raise ValueError('Username contains numbers')

        if len(password) >= 20:
            raise ValueError('Password is too long')
        if len(password) <= 8:
            raise ValueError('Password is too long')
        if len([x for x in password if x.isdigit()]) < 2:
            raise ValueError('Password must have at least 2 numbers')

        self.username = username
        self.password = password

class Users():
    def __init__(self):
        # TODO:
        pass

    def add_user(self, username, password):
        # TODO:
        pass

    def remove_user(self, username):
        # TODO:
        pass

    def list_all(self):
        # TODO:
        pass

