import tournament.player as player_module
import pandas as pd


class Tournament:
    file_path = ""
    players = []
    system = ""

    @staticmethod
    def get_tn_name(file_path):
        tournament_data = pd.read_excel(file_path, sheet_name="Турнирные данные")
        return tournament_data.columns[1]

    @staticmethod
    def get_referee_name(file_path):
        tournament_data = pd.read_excel(file_path, sheet_name="Турнирные данные")
        return tournament_data[tournament_data.columns[1]].tolist()[0]

    @staticmethod
    def get_assistant_referee_name(file_path):
        tournament_data = pd.read_excel(file_path, sheet_name="Турнирные данные")
        return tournament_data[tournament_data.columns[1]].tolist()[1]

    @staticmethod
    def get_system(file_path):
        tournament_data = pd.read_excel(file_path, sheet_name="Турнирные данные")
        return tournament_data[tournament_data.columns[1]].tolist()[2]

    @staticmethod
    def get_count_of_tours(file_path):
        tournament_data = pd.read_excel(file_path, sheet_name="Турнирные данные")
        return tournament_data[tournament_data.columns[1]].tolist()[3]

    @staticmethod
    def get_current_tour(file_path):
        tournament_data = pd.read_excel(file_path, sheet_name="Турнирные данные")
        return tournament_data[tournament_data.columns[1]].tolist()[4]

    @staticmethod
    def get_date_of_start(file_path):
        tournament_data = pd.read_excel(file_path, sheet_name="Турнирные данные")
        return tournament_data[tournament_data.columns[1]].tolist()[5]

    @staticmethod
    def get_date_of_end(file_path):
        tournament_data = pd.read_excel(file_path, sheet_name="Турнирные данные")
        return tournament_data[tournament_data.columns[1]].tolist()[6]

    @staticmethod
    def get_name_of_coefficient(name_of_system):
        return "Название коэффициента"

    @staticmethod
    def get_all_of_data_without_tn_name(file_path):
        tournament_data = pd.read_excel(file_path, sheet_name="Турнирные данные")
        return tuple(tournament_data[tournament_data.columns[1]].tolist())

    def add_player(self, number, name):
        self.players.append(player_module.Player(number, name))

    def add_players(self, players):
        self.players = players

    def sort_players(self):
        # Сортируем по количеству очков
        self.players.sort(key=lambda x: x.number_of_points, reverse=True)

        # При равенстве очков сортируем по приоритетам
        for i in range(len(self.players) - 1):
            if self.players[i].number_of_points == self.players[i + 1].number_of_points:
                pl_1 = self.players[i]
                pl_2 = self.players[i + 1]

                # Перебираем приоритеты, если один из приоритетов
                # оказался у одного игрока лучше, чем у другого, делам
                # соответствующее действие и выходим из цикла перебора приоритетов
                tournament_data = pd.read_excel(self.file_path, sheet_name="Турнирные данные")
                pr1, pr2, pr3, pr4 = tuple(tournament_data[tournament_data.columns[1]].tolist()[-4:])

                for pr in [pr1, pr2, pr3, pr4]:
                    if pl_1.check_priority(pr, pl_2) < pl_2.check_priority(pr, pl_1):
                        self.players[i], self.players[i + 1] = self.players[i + 1], self.players[i]
                        break
                    elif pl_1.check_priority(pr1, pl_2) > pl_2.check_priority(pr1, pl_1):
                        break

    def draw(self):
        # В случае нечётного количества игроков добавляем фиктвного участника.
        # Если в прошлом туре добавили нового игрока, то при наличии фиктивного - удаляем его
        delete_plus = False
        if len(self.players) % 2 != 0:
            for player in self.players:
                if player.name == "+":
                    self.players.remove(player)
                    delete_plus = True
                    break
            if not delete_plus:
                self.players.append(player_module.Player(len(self.players) + 1, "+"))

        # В словаре pairs: ключ - игрок, играющий белым цветом, значение - черным
        pairs = {}
        self.sort_players()

        max_number_of_points = self.players[0].number_of_points
        groups = [[] for _ in range(len(self.players))]
        index_of_group = 0

        # Распределяем игроков по группам с одинаковым количеством очков
        for player in self.players:
            if player.number_of_points != max_number_of_points:
                index_of_group += 1
                max_number_of_points = player.number_of_points
            groups[index_of_group].append(player)

        # Удаляем лишние, пустые группы
        groups = groups[0:index_of_group + 1]

        for index in range(index_of_group + 1):
            # copig - count_of_players_in_group
            copig = len(groups[index])

            for index_of_player in range(copig):
                # Игроки, которые уже были распределены в пары
                players_in_pairs = list(pairs.keys()) + list(pairs.values())

                # groups[index][index_of_player] - текущий игрок
                # Если текущего игрока ещё не распределили,
                # то первым игроком в новой паре становится он,
                # и далее для первого игрока мы ищем его соперника
                if players_in_pairs.count(groups[index][index_of_player]) == 0:
                    first_player: player_module.Player = groups[index][index_of_player]
                    # Так как список оппонентов представлен
                    # как список кортежей и мы должны получить
                    # только игроков, то необходимо транспонировать
                    # наш список списков и взять первый элемент
                    if len(first_player.list_of_opponents) > 0:
                        list_of_opponents = first_player.list_of_opponents[::, 0]
                    else:
                        list_of_opponents = []
                    second_player = None
                    # Вначале ищем второго игрока среди второй части текущей группы
                    for index_of_second_part_group in range(copig // 2 + copig % 2, copig):
                        current_player_2 = groups[index][index_of_second_part_group]
                        # Если текущий игрок ещё не находится в паре
                        # и он не играл с уже выбранным первым игроком,
                        # то мы нашли второго игрока
                        if players_in_pairs.count(current_player_2) == 0 and current_player_2 != first_player:
                            if list_of_opponents.count(current_player_2) == 0:
                                second_player = current_player_2
                                break
                    # Если мы не нашли второго игрока среди
                    # второй части текущей группы, то ищем
                    # его среди первой части текущей группы
                    if second_player is None:
                        for index_of_first_part_group in range(0, copig // 2 + copig % 2):
                            current_player_2 = groups[index][index_of_first_part_group]
                            if current_player_2 not in players_in_pairs and current_player_2 not in list_of_opponents and current_player_2 != first_player:
                                second_player = current_player_2
                                break
                    # Если для первого игрока не нашлось соперника из текущей группы,
                    # то отправляем данного игрока в следующую группу
                    if second_player is None:
                        if index + 1 < len(groups):
                            groups[index + 1].insert(0, first_player)
                        # Удалять игрока из текущей группы нет смысла,
                        # так как с ним в любом случае никто не сможет
                        # встать в пару (так как никто не подошел к нему)
                        continue

                    # В противном случае мы нашли соперника.
                    # Если первый игрок играл белым цветом чаще,
                    # чем второй, даём второму белый цвет
                    if first_player.get_count_of_white_games() >= second_player.get_count_of_white_games():
                        pairs[first_player] = second_player
                    else:
                        pairs[second_player] = first_player

        if len(pairs) * 2 == len(self.players):
            return pairs
        else:
            # Список возможных пар имеет вид: [(player_1, player_2), (player_3, player_4), ...]
            list_of_possible_pairs = []

            # Список игроков с количеством возможных
            # оппонентов из последней группы вида:
            # [(player_1, count_of_opponents), (player_2, count_of_opponents), ...]
            counts_of_possible_opponents = []

            # Удаляем из итогового списка пар те пары, которые
            # были составлены из игроков последней группы, а
            # также составляем список всех рёбер
            # (возможных пар) последней группы и заполняем
            # counts_of_possible_opponents
            for player in groups[-1]:
                # Второй параметр None необходим, чтобы не выбрасывалось исключение
                pairs.pop(player, None)
                list_of_opponents = player.list_of_opponents[::, 0]
                counts_of_possible_opponents.append((player, 0))
                for player_2 in groups[-1]:
                    if player_2 not in list_of_opponents \
                            and player_2 != player \
                            and [player, player_2] not in list_of_possible_pairs:
                        list_of_possible_pairs.append((player, player_2))
                        counts_of_possible_opponents[-1][1] += 1

            # Сортируем игроков по количеству возможных пар в обратном порядке
            counts_of_possible_opponents.sort(key=lambda x: x[1])

            # Чтобы распределить всех игроков, необходимо вначале распределить тех,
            # у кого наименьшее количество возможных пар
            distributed_players = []

            for player, count in counts_of_possible_opponents:
                for pair in list_of_possible_pairs:
                    # Если мы нашли пару, где один из игроков - тот,
                    # которого должны распределить, а также мы не распределяли
                    # его и пару, то делаем это и добавляем их в
                    # список распределенных игроков
                    if (pair[0] == player or pair[1] == player) and distributed_players.count(pair[0]) == 0\
                            and distributed_players.count(pair[1]) == 0:
                        if pair[0].get_count_of_white_games() >= pair[1].get_count_of_white_games():
                            pairs[pair[1]] = pair[0]
                        else:
                            pairs[pair[0]] = pair[1]
                        distributed_players.append(pair[0])
                        distributed_players.append(pair[1])

            return pairs
