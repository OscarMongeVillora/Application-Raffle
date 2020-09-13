import datetime
import random
from ad import Ad

class Raffle(object):

    def __init__(self, id_raffle: str, name: str, ad: Ad, duration: float = 60):
        self._id_raffle = id_raffle
        self._name_raffle = name
        self._ad = ad  # Ojeto anuncio Asociado
        self._id_ad = ad.show_properties()[0]
        self._started = 0
        self._finished = 0

        self._time_duration = duration  # Seconds of a day
        self._time_start = 0
        self._time_raffle = 0
        self._time_stop = 0

        self._prize_money = 0
        self._participants = list()
        self._id_participants = list()
        self._number_winners = 1
        self._id_winners = list()
        self._winners = list()

    def start_zerotime_raffle(self):
        self._time_start = datetime.now()
        self._time_raffle = self._time_duration + datetime.timestamp(self._time_start)  # Add the duration
        self._time_stop = datetime.fromtimestamp(self._time_raffle)
        self._started = 1

    def get_ad_associated(self):
        return self._ad

    def calculate_prize_money(self):
        if self.show_availability():
            self._prize_money = float(self._ad.show_properties()[2]) * float(self._ad.show_properties()[3])
            return self._prize_money
        else:
            print('The raffle has not started, the ad is not available')

    def show_properties(self):
        print(' The prize money is: {}'.format(self._prize_money), '\n',
              'The duration of the raffle is {} seconds'.format(self._time_duration), '\n',
              'It finishes at {}'.format(self._time_stop), '\n',
              'The number of winners is {}'.format(self._number_winners))

    def get_properties(self):
        properties_dict = {'name': self._name_raffle, 'money': self._prize_money, 'id_raffle': self._id_raffle,
                           'duration': self._time_duration, 'time_raffle': self._time_stop,
                           'number_winners': self._number_winners}
        return properties_dict

    def show_availability(self):
        return self._started == 1

    def get_finished(self):
        return self._finished == 1

    def refresh_raffle(self):
        if (self._started == 1) & (datetime.now() > self._time_stop):
            self.raffle_select_winners()

    def raffle_select_winners(self):
        if self._finished == 1:  # I protect the method to avoid to repeat the specific raffle
            pass
            # return self._winners
        else:
            self._participants = self._ad.export_users()
            self._id_participants = [x.check_profile()[0] for x in self._participants]
            self._id_winners = random.sample(self._id_participants, k=self._number_winners)
            self._winners = [x for x in self._participants if x.check_profile()[0] in self._id_winners]
            self._finished = 1

            # return self._winners

    def announce_winners(
            self):  # Here will be the graphics of the raffle, this method have to be automatic when the app starts

        if self._finished == 1:
            print('The winners are {} from {} with a prize per winner of {} €' \
                  .format([x.check_profile()[2] for x in self._winners],
                          [x.check_profile()[3] for x in self._winners],
                          self._prize_money / self._number_winners))

        elif self._started == 1:
            time_check = datetime.timestamp(datetime.now())
            remain_time = self._time_raffle - time_check
            print('The raffle has not been finished, the winners will be choosed in {} hours, {} minutes, {} seconds' \
                  .format(round(remain_time / 60 / 60), round(remain_time / 60),
                          remain_time - round(round(remain_time / 60) * 60)))

        else:
            print('The raffle has not started')

    def get_winners(self):
        return self._winners