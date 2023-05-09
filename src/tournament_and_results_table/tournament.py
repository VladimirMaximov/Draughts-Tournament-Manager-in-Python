import tournament_and_results_table as tart


class Tournament:

    def __init__(self, tournament_name="", referee_name="", assistant_referee_name="",
                 system="", count_of_tours="", count_of_parties="",
                 date="", priority_1="", priority_2="", priority_3="", priority_4=""):
        self.tournament_name = tournament_name
        self.referee_name = referee_name
        self.assistant_referee_name = assistant_referee_name
        self.system = system
        self.count_of_tours = count_of_tours
        self.count_of_parties = count_of_parties
        self.date = date
        self.priority_1 = priority_1
        self.priority_2 = priority_2
        self.priority_3 = priority_3
        self.priority_4 = priority_4
        self.current_tour = 1
        self.players = []

    def add_player(self, name):
        self.players.append(tart.Player(name, 0, [], 0, 0, 0))

    def add_players(self, players):
        self.players = players

    def draw(self):
        # В случае нечётного количества игроков добавляем фиктвного участника.
        # Если в прошлом туре добавили нового игрока, то при наличии фиктивного - удаляем его
        even_number_of_players = len(self.players) % 2 == 0
        if not even_number_of_players and self.players.count(tart.Player("+")) == 0:
            self.players.append(tart.Player("+"))
        elif not even_number_of_players and self.players.count(tart.Player("+")) == 1:
            self.players.remove(tart.Player("+"))

        # В словаре pairs: ключ - игрок, играющий белым цветом, значение - черным
        pairs = {}
        self.players.sort(key=lambda x: x.number_of_points, reverse=True)

        max_number_of_points = self.players[0].number_of_points
        groups = [[]] * len(self.players)
        index_of_group = 0

        # Распределяем игроков по группам с одинаковым количеством очков
        for player in self.players:
            if player.number_of_points != max_number_of_points:
                index_of_group += 1
                max_number_of_points = player.number_of_points

            groups[index_of_group].append(player)

        # Удаляем лишние, пустые группы
        groups = groups[0:index_of_group + 1]

        for index_of_group in range(index_of_group + 1):
            # copig - count_of_players_in_group
            copig = len(groups[index_of_group])

            for index_of_player in range(copig):
                # Игроки, которые уже были распределены в пары
                players_in_pairs = list(pairs.keys()) + list(pairs.values())
                # Текущий игрок - тот, которого мы хотим распределить в пару
                current_player = groups[index_of_group][index_of_player]

                # Если текущего игрока ещё не распределили,
                # то первым игроком в новой паре становится он,
                # и далее для первого игрока мы ищем его соперника
                if players_in_pairs.count(current_player) == 0:
                    first_player = current_player
                    # Так как список оппонентов представлен
                    # как список списков и мы должны получить
                    # только игроков, то необходимо транспонировать
                    # наш список списков и взять первый элемент
                    if len(first_player.list_of_opponents) > 0:
                        list_of_opponents = list(map(list, zip(*first_player.list_of_opponents)))[0]
                    else:
                        list_of_opponents = []

                    second_player = None
                    # Вначале ищем второго игрока среди второй части текущей группы
                    for index_of_second_part_group in range(copig // 2 + copig % 2, copig):
                        current_player = groups[index_of_group][index_of_second_part_group]
                        # Если текущий игрок ещё не находится в паре
                        # и он не играл с уже выбранным первым игроком,
                        # то мы нашли второго игрока
                        if players_in_pairs.count(current_player) == 0 and current_player != first_player:
                            if list_of_opponents.count(current_player) == 0:
                                second_player = current_player
                                break

                    # Если мы не нашли второго игрока среди
                    # второй части текущей группы, то ищем
                    # его среди первой части текущей группы
                    if second_player is None:
                        for index_of_first_part_group in range(0, copig // 2 + copig % 2):
                            current_player = groups[index_of_group][index_of_first_part_group]

                            if players_in_pairs.count(current_player) == 0 and list_of_opponents.count(current_player) == 0 and current_player != first_player:
                                second_player = current_player
                                break

                    # Если для первого игрока не нашлось соперника из текущей группы,
                    # то отправляем данного игрока в следующую группу
                    if second_player is None:
                        if index_of_group + 1 < len(groups):
                            groups[index_of_group + 1].insert(0, first_player)
                        # Удалять игрока из текущей группы нет смысла,
                        # так как с ним в любом случае никто не сможет
                        # встать в пару (так как никто не подошел к нему)
                        continue

                    # Если первый игрок играл белым цветом чаще,
                    # чем второй, даём второму белый цвет
                    if first_player.last_game_color >= second_player.last_game_color:
                        pairs[second_player] = first_player
                        first_player.last_game_color -= 1
                        second_player.last_game_color += 1
                    else:
                        pairs[first_player] = second_player
                        first_player.last_game_color += 1
                        second_player.last_game_color -= 1

        return pairs
