class Player:

    def __init__(self, number, name, list_of_opponents: list = None, number_of_points=0, place=None):
        self.number = number  # Порядковый номер
        self.name = name

        # Список оппонентов - список вида:
        # [[opponent_1, color_1, result_1], [opponent_2, color_2, result_2], ...]
        if list_of_opponents is None:
            self.list_of_opponents = []
        else:
            self.list_of_opponents = list_of_opponents

        self.number_of_points = number_of_points
        self.place = place

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def get_count_of_white_games(self):
        if self.list_of_opponents:
            return list(list(zip(*self.list_of_opponents))[1]).count("w")
        else:
            return 0

    systems_of_coefficients = ["Система коэффициентов Шмульяна",
                               "Cистема коэффициентов Бухгольца",
                               "Медианный коэффициент Солкофа",
                               "Короткий усеченный коэффициент Солкофа",
                               "Полный усеченный коэффициент Солкофа"]

    def get_coefficient(self, name_of_coefficient):
        if name_of_coefficient == "Наибольшее число побед":
            return self.get_count_of_wins()
        elif name_of_coefficient == "Коэффициент Шмульяна":
            return self.get_schmullan_coefficient()
        elif name_of_coefficient == "Коэффициент Бухгольца":
            return self.get_buchholz_coefficient()
        elif name_of_coefficient == "Медианный коэффициент Солкофа":
            return self.get_median_solkoff_coefficient()
        elif name_of_coefficient == "Полный усеченный коэффициент Солкофа":
            return self.get_full_truncated_solkoff_coefficient()
        elif name_of_coefficient == "Короткий усеченный коэффициент Солкофа":
            return self.get_short_truncated_solkoff_coefficient()
        else:
            return 0

    # Также передаем оппонента, так как
    # возможна проверка личной встречи
    def check_priority(self, priority: str, opponent):
        if priority == "Результат личной встречи":
            for opponent_from_list in self.list_of_opponents:
                if opponent_from_list[0] == opponent:
                    return opponent_from_list[2]
            return 0
        else:
            return self.get_coefficient(priority)

    def get_count_of_wins(self):
        res = 0
        for opponent, result, color in self.list_of_opponents:
            if result == 2:
                res += 1
        return res

    def get_schmullan_coefficient(self):
        winner_points = 0
        loser_points = 0

        for opponent, result, color in self.list_of_opponents:
            if result == 2:
                winner_points += opponent.number_of_points
            if result == 0:
                loser_points += opponent.number_of_points

        return winner_points - loser_points

    def get_buchholz_coefficient(self):
        res = 0

        for opponent, result, color in self.list_of_opponents:
            res += opponent.number_of_points

        return res

    def get_median_solkoff_coefficient(self):
        res_of_opponents = []
        for opponent, result, color in self.list_of_opponents:
            res_of_opponents.append(opponent.number_of_points)

        res_of_opponents.sort()

        if len(res_of_opponents) <= 2:
            return 0
        else:
            return sum(res_of_opponents[1:-1])

    def get_short_truncated_solkoff_coefficient(self):
        return self.get_full_truncated_solkoff_coefficient()[0]

    def get_full_truncated_solkoff_coefficient(self):

        res_of_opponents = []
        for opponent, result, color in self.list_of_opponents:
            res_of_opponents.append(opponent.number_of_points)

        res_of_opponents.sort()
        return [sum(res_of_opponents[i::]) for i in range(1, len(res_of_opponents))]
