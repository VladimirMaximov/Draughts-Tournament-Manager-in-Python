import tournament_and_results_table as tart
import pandas as pd

class Tournament:
    file_path = ""
    players = []

    def create_new_tournament(self, directory_path, tn_name):
        pass

    def get_tn_name(self):
        pass

    def get_referee_name(self):
        pass

    def get_assistant_referee_name(self):
        pass

    def get_system(self):
        pass

    def get_count_of_tours(self):
        pass

    def get_current_tour(self):
        pass

    def get_date_of_start(self):
        pass

    def get_date_of_end(self):
        pass

    def get_priority_1(self):
        pass

    def get_priority_2(self):
        pass

    def get_priority_3(self):
        pass

    def get_priority_4(self):
        pass

    def add_player(self, name):
        self.players.append(tart.Player(name, 0, [], 0, 0, 0))

    def add_players(self, players):
        self.players = players

    def sort_players(self, without_latter: bool = False):
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
                for priority in [self.priority_1, self.priority_2, self.priority_3, self.priority_4]:
                    if pl_1.check_priority(priority, pl_2, without_latter) < pl_2.check_priority(priority, pl_1,
                                                                                                 without_latter):
                        self.players[i], self.players[i + 1] = self.players[i + 1], self.players[i]
                        break
                    elif pl_1.check_priority(self.priority_1, pl_2, without_latter) > pl_2.check_priority(
                            self.priority_1, pl_1, without_latter):
                        break

    def draw(self):
        # В случае нечётного количества игроков добавляем фиктвного участника.
        # Если в прошлом туре добавили нового игрока, то при наличии фиктивного - удаляем его
        delete_plus = False
        if not len(self.players) % 2 == 0:
            for player in self.players:
                if player.name == "+":
                    self.players.remove(player)
                    delete_plus = True
                    break
            if not delete_plus:
                self.players.append(tart.Player("+"))

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

        for index_of_group in range(index_of_group + 1):
            # copig - count_of_players_in_group
            copig = len(groups[index_of_group])

            for index_of_player in range(copig):
                # Игроки, которые уже были распределены в пары
                players_in_pairs = list(pairs.keys()) + list(pairs.values())

                # groups[index_of_group][index_of_player] - текущий игрок
                # Если текущего игрока ещё не распределили,
                # то первым игроком в новой паре становится он,
                # и далее для первого игрока мы ищем его соперника
                if players_in_pairs.count(groups[index_of_group][index_of_player]) == 0:
                    first_player = groups[index_of_group][index_of_player]
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
                        current_player_2 = groups[index_of_group][index_of_second_part_group]
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
                            current_player_2 = groups[index_of_group][index_of_first_part_group]
                            if current_player_2 not in players_in_pairs and current_player_2 not in list_of_opponents and current_player_2 != first_player:
                                second_player = current_player_2
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

        if len(pairs) * 2 == len(self.players):
            return pairs
        else:
            list_of_possible_pairs = []
            visited = [False] * len(groups[-1])
            result_traversing = []
            # Удаляем из итогового списка пар те пары, которые
            # были составлены из игроков последней группы, а
            # также составляем список всех рёбер
            # (возможных пар) последней группы
            for player in groups[-1]:
                pairs.pop(player, None)
                list_of_opponents = list(map(list, zip(*player.list_of_opponents)))[0]
                for player_2 in groups[-1]:
                    if player_2 not in list_of_opponents \
                            and player_2 != player \
                            and [player, player_2] not in list_of_possible_pairs:
                        list_of_possible_pairs.append((player, player_2))

            # Реализуем алгоритм обхода в глубину
            def next_vertex(next_player: tart.Player):
                # Проверяем посещали ли мы вершину
                if not visited[groups[-1].index(next_player)]:
                    # Если нет, тогда добавляем вершину в итоговый список
                    result_traversing.append(next_player)
                    # Указываем, что мы её посетили
                    visited[groups[-1].index(next_player)] = True
                    # Для всех вершин, смежных данной вершине запускаем функцию
                    for edge in list_of_possible_pairs:
                        if edge[0] == next_player:
                            next_vertex(edge[1])

            next_vertex(groups[-1][0])
            # Составляем из списка result_traversing
            # пары и добавляем их в итоговый список pairs
            for i in range(0, len(result_traversing), 2):
                first_player = result_traversing[i]
                second_player = result_traversing[i + 1]

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
