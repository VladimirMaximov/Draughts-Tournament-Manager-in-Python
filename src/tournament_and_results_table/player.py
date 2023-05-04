

class Player:

    def __init__(self, name, number_of_points, list_of_opponents,
                 number_of_wins, schmullan_coefficient, buchholz_coefficient):
        self.name = name
        self.number_of_points = number_of_points
        self.list_of_opponents = list_of_opponents
        self.number_of_wins = number_of_wins
        self.schmullan_coefficient = schmullan_coefficient
        self.buchholz_coefficient = buchholz_coefficient
