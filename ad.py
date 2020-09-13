from user import User


class Ad(object):

    def __init__(self, id_ad: str, company: str, cost_per_visit: float):
        self._id_ad = id_ad
        self._company = company
        self._cost_per_visit = cost_per_visit
        self._users_seen = set()
        self._number_visits = len(self._users_seen)

    def visualize(self, user: User) -> None:  # An user can only register one visualization
        # self._users_seen.append((user.check_id_name()[0])
        self._users_seen.add(user)  # Creo una lista de objetos Usuarios
        self._number_visits = len(self._users_seen)

    def show_properties(self):
        return [self._id_ad, self._company, self._cost_per_visit, self._number_visits]

    def export_users(self):
        return list(self._users_seen)