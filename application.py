from user import User
from ad import Ad
from raffle import Raffle



class App(object):  # An object of this class has to be used by any user, more than one users can be connected at the same time


    # However each user is using the App in his phone, so is opening a new sentence of App
    # Only activate one time for user as the installation

    def __init__(self, list_users: [User], list_ads: [Ad], list_raffles: [Raffle]):
        self._users = {user.check_profile()[0]: user for user in list_users}
        self._users_nick_id = {user.check_profile()[1]: user.check_profile()[0] for user in list_users}
        self._ads = list_ads
        self._raffles = list_raffles
        self._main_user = object()
        self._available_raffles = list()
        self._finished_raffles = list()
        self._user_connected = 0
        self._raffle_prized_list = list()
        self._prize = 0
        self._winners_raffle_prize = list()
        self._winners = list()
        self._raffles_win = list()
        self._raffles_final_prize_euros = list()


    def connect(self, main_nick: str, password: str):  # Lo pasaría el usuario
        if self._user_connected == 1:
            print('You are already connected {}'.format(main_nick))
            self.refresh()
        else:
            # password = input('Introduce your password: ')
            User = self._users[self._users_nick_id[main_nick]]
            if password == User._validate_password():
                self._main_user = User
                self._user_connected = 1
                print('You are connected now')
                self.refresh()


    def disconnect(self):
        if self._user_connected == 1:
            self._user_connected = 0
        else:
            print('You are not connected already')


    def see_available_raffles(self):  # Generar grafica datos
        self.refresh()

        if self._user_connected == 1:
            screen_raffle = [x.get_properties() for x in self._available_raffles.values() \
                             if
                             x not in self._finished_raffles.values()]  # Con este if evitamos que vean sorteos ya premiados
            return screen_raffle
        else:
            print('You are not logged in the App')


    def choose_raffle(self, name_raffle: str):  # You select with a push button the raffle
        self.refresh()

        if self._user_connected == 1:
            raffle_choosen = self._available_raffles[name_raffle]  # If I want to choose with the Id I need to change how I
            # create the dictionary
            # question = input('Do you want to participate in the raffle? Write (y/n) ')
            question = 'y'

            if question == 'y':
                self._participate_raffle(raffle_choosen)
                print('You are participating in the {}.'.format(name_raffle))
                return raffle_choosen.get_properties()
            else:
                print('Okey, is your decision')

        else:
            print('You are not logged in the App')


    def _participate_raffle(self, raffle_choosen: Raffle):  # I want this method to be private and we can only access since
        if self._user_connected == 1:  # choose_raffle
            ad_associated = raffle_choosen.get_ad_associated()
            ad_associated.visualize(user=self._main_user)

        else:
            print('You are not logged in the App')


    def refresh(self):
        [raffle.refresh_raffle() for raffle in self._raffles if raffle.show_availability()]

        self._available_raffles = {raffle.get_properties()['name']: raffle for raffle in self._raffles \
                                   if raffle.show_availability()}

        self._finished_raffles = {raffle.get_properties()['name']: raffle for raffle in self._raffles \
                                  if (raffle.show_availability() & raffle.get_finished())}

        self._winners_raffle_prize = [(winners, raffle, raffle.calculate_prize_money()) for raffle \
                                      in self._finished_raffles.values() for winners in raffle.get_winners()]
        # 2 comprensiones de lista

        # Estos 3 vectores estan ordenados a la vez
        self._winners = [tuples[0].check_profile()[2] for tuples in self._winners_raffle_prize]  # Select name
        self._raffles_win = [tuples[1].get_properties()['name'] for tuples in self._winners_raffle_prize]
        self._raffles_final_prize_euros = [tuples[2] for tuples in self._winners_raffle_prize]
        # Compongo un dataframe con estos 3 vectores
        self._rank_winner = pd.DataFrame({'Winners': self._winners, 'Raffle': self._raffles_win,
                                          'Prize (€)': self._raffles_final_prize_euros})


    def collect_prize(self, password: str):
        self.refresh()
        if self._user_connected == 1:
            if self._main_user.check_profile()[2] in self._winners:

                raffle_prize = [raffle for raffle in self._finished_raffles.values() \
                                if (raffle.get_winners() == self._main_user)]

                for raffle in raffle_prize:
                    if raffle in self._raffle_prized_list:
                        self._prize = 0
                    else:
                        self._prize += raffle.calculate_prize_money()
                        self._raffle_prized_list.append(raffle)

                if self._prize == 0:
                    print('Your prize has been paid and you have not win any more prizes')
                else:
                    # password = str(input('Introduce your password'))
                    self._pay_bizum(self._main_user.check_profile()[1], password, self._prize)
            else:
                print('You have not win any prize yet')
        else:
            print('You are not logged in the App')


    def see_main_user(self):
        return self._main_user.check_profile()


    def _pay_bizum(self, nick: str, password: str, money: float):
        bizum = self._main_user.obtain_bizum(nick, password)
        print('The prize of {} € has been paid to the user {} of bizum {}'.format(money, nick, bizum))


    def see_winners(self):
        self.refresh()
        return self._rank_winner
