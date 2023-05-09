
class Player:

    def __init__(self, name, number_of_points=0, list_of_opponents=None,
                 number_of_wins=0, schmullan_coefficient=0, buchholz_coefficient=0):
        self.name = name
        self.number_of_points = number_of_points
        # Список оппонентов представлен как список кортежей,
        # где каждый кортеж имеет 2 элемента -
        # игрока и результат при игре с ним
        if list_of_opponents is None:
            self.list_of_opponents = []
        else:
            self.list_of_opponents = list_of_opponents
        self.number_of_wins = number_of_wins
        self.schmullan_coefficient = schmullan_coefficient
        self.buchholz_coefficient = buchholz_coefficient
        # Принимает значение n, если n < 0, значит игрок больше
        # сыграл партий чёрным цветом, если n > 0 - белым
        self.last_game_color = 0

    def set_schmullan_coefficient(self):
        winner_points = 0
        loser_points = 0

        for opponent, result in self.list_of_opponents:
            if result == 2:
                winner_points += opponent.number_of_points
            if result == 0:
                loser_points += opponent.number_of_points

        self.schmullan_coefficient = abs(winner_points - loser_points)

    def set_buchholz_coefficient(self):
        result = 0

        for opponent, result in self.list_of_opponents:
            result += opponent.number_of_points

        self.buchholz_coefficient = result
