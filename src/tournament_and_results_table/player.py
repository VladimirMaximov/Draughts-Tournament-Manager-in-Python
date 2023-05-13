class Player:

    def __init__(self, name, number_of_points=0, list_of_opponents=None,
                 number_of_wins=0, schmullan_coefficient=0, buchholz_coefficient=0):
        self.name = name
        self.number_of_points = number_of_points
        # Список оппонентов представлен как список кортежей,
        # где каждый кортеж имеет 3 элемента -
        # игрока, результат при игре с ним и цвет
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

    def check_priority(self, priority: str, opponent, without_latter: bool = False):
        if priority == "Результат личной встречи":
            for opponent_from_list in self.list_of_opponents:
                if opponent_from_list[0] == opponent:
                    return opponent_from_list[1]
            return 0
        elif priority == "Наибольшее число побед":
            return self.number_of_wins
        elif priority == "Система коэффициентов Шмульяна":
            self.set_schmullan_coefficient(without_latter)
            return self.schmullan_coefficient
        elif priority == "Система коэффициентов Бухгольца":
            self.set_buchholz_coefficient(without_latter)
            return self.buchholz_coefficient
        else:
            return 0

    def set_schmullan_coefficient(self, without_latter: bool = False):
        winner_points = 0
        loser_points = 0
        # Если мы считаем коэффициент после того,
        # как вернулись на тур назад, то делаем
        # это не включая последнего соперника
        if without_latter:
            list_of_opponents = self.list_of_opponents[:-1]
        else:
            list_of_opponents = self.list_of_opponents

        for opponent, result, color in list_of_opponents:
            if result == 2:
                winner_points += opponent.number_of_points
            if result == 0:
                loser_points += opponent.number_of_points

        self.schmullan_coefficient = abs(winner_points - loser_points)

    def set_buchholz_coefficient(self, without_latter: bool = False):
        result = 0
        # Если мы считаем коэффициент после того,
        # как вернулись на тур назад, то делаем
        # это не включая последнего соперника
        if without_latter:
            list_of_opponents = self.list_of_opponents[:-1]
        else:
            list_of_opponents = self.list_of_opponents

        for opponent in list_of_opponents:
            result += opponent[0].number_of_points

        self.buchholz_coefficient = result
