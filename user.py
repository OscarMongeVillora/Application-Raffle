from typing import Tuple

class User(object):

    def __init__(self, id_user: float, nick: str, name: str, bizum: float, location: str):
        self._id_user = id_user
        self._name = name
        self._nick = nick
        self._bizum = bizum
        self._location = location
        self._password = 0
        self._configured = 0

    def set_password(self, password: str) -> None:
        # self._password = str(input('Introduce your password of 5 digits: '))
        self._password = password
        if len(self._password) != 5:
            raise ValueError('Your password is not constructed using 5 digits, repeat again')
        self._configured = 1
        print('Password accepted')

    def _validate_password(self):
        if self._configured == 1:
            return self._password
        else:
            print('You are not validated in our datebase')

    def user_configured(self):
        if self._configured == 1:
            return True
        else:
            return False

    def check_profile(self) -> Tuple[str, str, str, str]:
        return self._id_user, self._nick, self._name, self._location

    def obtain_bizum(self, nick: str, password: str) -> float:
        if self._nick == nick:
            if self._password == password:
                return self._bizum
            else:
                raise ValueError('Your password is incorrect')
        else:
            raise ValueError('This nick not exist')