class Player:

    def __init__(self, number, name, list_of_opponents=None, number_of_points=0,
                 number_of_wins=0, schmullan_coefficient=0, buchholz_coefficient=0, place=None):
        self.number = number  # Порядковый номер
        self.name = name
        if list_of_opponents is None:
            self.list_of_opponents = []
        else:
            self.list_of_opponents = list_of_opponents

        self.number_of_points = number_of_points
        self.number_of_wins = number_of_wins
        self.schmullan_coefficient = schmullan_coefficient
        self.buchholz_coefficient = buchholz_coefficient
        self.place = place

    def __eq__(self, other):
        return self.name == other.name

    # Также передаем оппонента, так как
    # возможна проверка личной встречи
    def check_priority(self, priority: str, opponent):
        if priority == "Результат личной встречи":
            for opponent_from_list in self.list_of_opponents:
                if opponent_from_list[0] == opponent:
                    return opponent_from_list[1]
            return 0
        elif priority == "Наибольшее число побед":
            return self.number_of_wins
        elif priority == "Система коэффициентов Шмульяна":
            self.set_schmullan_coefficient()
            return self.schmullan_coefficient
        elif priority == "Система коэффициентов Бухгольца":
            self.set_buchholz_coefficient()
            return self.buchholz_coefficient
        else:
            return 0

    def set_schmullan_coefficient(self):
        winner_points = 0
        loser_points = 0

        list_of_opponents = self.list_of_opponents

        for opponent, result, color in list_of_opponents:
            if result == 2:
                winner_points += opponent.number_of_points
            if result == 0:
                loser_points += opponent.number_of_points

        self.schmullan_coefficient = abs(winner_points - loser_points)

    def set_buchholz_coefficient(self):
        result = 0

        for opponent in self.list_of_opponents:
            result += opponent.number_of_points

        self.buchholz_coefficient = result

    def set_median_solkoff_coefficient(self):
        result = 0

        minimal_result = 10000000
        maximal_result = -1

        for opponent in self.list_of_opponents:
            result += opponent.number_of_points

            if opponent.number_of_points < minimal_result:
                minimal_result = opponent.number_of_points

            if opponent.number_of_points > maximal_result:
                maximal_result = opponent.number_of_points

        return result - minimal_result - maximal_result

    def set_median_solkoff_coefficient(self):
        result = 0

        minimal_result = 10000000
        maximal_result = -1

        for opponent in self.list_of_opponents:
            result += opponent.number_of_points

            if opponent.number_of_points < minimal_result:
                minimal_result = opponent.number_of_points

            if opponent.number_of_points > maximal_result:
                maximal_result = opponent.number_of_points

        return result - minimal_result - maximal_result



