import tournament.player as player_module
import pandas as pd


class Tournament:
    def __init__(self, file_path="", players=None):
        if players is None:
            players = []
        self.file_path = file_path
        self.players = players

    def fill_tour(self):

        tournament_data = pd.read_excel(self.file_path, sheet_name="Основная таблица")
        count_of_tours = int(self.get_count_of_tours())
        current_tour = int(self.get_current_tour())

        # Первые 2 столбца таблицы
        main_table_1 = pd.DataFrame({"Номер": tournament_data[tournament_data.columns[0]].tolist(),
                                     "ФИО": tournament_data[tournament_data.columns[1]].tolist()
                                     })

        # Если прошло больше одного тура, то вначале формируем
        # уже имеющиеся туры, а после добавляем к ним новый тур
        if current_tour > 1:
            main_table_2 = pd.DataFrame({tournament_data.columns[i]: tournament_data[tournament_data.columns[i]].tolist()
                                         for i in range(2, current_tour + 1)})
            main_table_3 = pd.DataFrame({tournament_data.columns[current_tour + 1]: self.create_last_tour_str_results()})
            main_table_2 = main_table_2.join(main_table_3)
        else:
            main_table_2 = pd.DataFrame(
                {tournament_data.columns[current_tour + 1]: self.create_last_tour_str_results()})

        # Заполняем будущие туры
        if current_tour < count_of_tours:
            main_table_3 = pd.DataFrame({f"Тур {i}": [] for i in range(current_tour + 1, count_of_tours + 1)})
            main_table_2 = main_table_2.join(main_table_3)

        pr1 = self.get_priority_1()
        pr2 = self.get_priority_2()
        pr3 = self.get_priority_3()
        pr4 = self.get_priority_4()

        main_table_3 = pd.DataFrame({"Всего очков": [player.number_of_points for player in self.players],
                                     pr1: [player.get_coefficient(pr1) for player in self.players],
                                     pr2: [player.get_coefficient(pr2) for player in self.players],
                                     pr3: [player.get_coefficient(pr3) for player in self.players],
                                     pr4: [player.get_coefficient(pr4) for player in self.players],
                                     "Место": [player.place for player in self.players]})

        main_table_1 = main_table_1.join(main_table_2).join(main_table_3)

        writer = pd.ExcelWriter(self.file_path, engine="openpyxl", mode="a", if_sheet_exists='replace')
        main_table_1.to_excel(writer, sheet_name="Основная таблица", index=False)

        writer.close()

    def create_last_tour_str_results(self):
        result_table = []

        # Сортируем игроков в соответствии с их номером
        self.players.sort(key=lambda x: x.number)

        for player in self.players:
            opponent, color, result = player.list_of_opponents[-1]
            result_table.append(str(opponent.number) + color + str(result))

        return result_table

    def prize_distribution(self):

        # Сортируем в порядке количества очков
        # и величины коэффициентов
        self.sort_players()

        for i, player in enumerate(self.players):
            player.place = i + 1

        self.players.sort(key=lambda x: x.number)

    def get_tn_name(self):
        tournament_data = pd.read_excel(self.file_path, sheet_name="Турнирные данные")
        return tournament_data.columns[1]

    def get_referee_name(self):
        tournament_data = pd.read_excel(self.file_path, sheet_name="Турнирные данные")
        return tournament_data[tournament_data.columns[1]].tolist()[0]

    def get_assistant_referee_name(self):
        tournament_data = pd.read_excel(self.file_path, sheet_name="Турнирные данные")
        return tournament_data[tournament_data.columns[1]].tolist()[1]

    def get_system(self):
        tournament_data = pd.read_excel(self.file_path, sheet_name="Турнирные данные")
        return tournament_data[tournament_data.columns[1]].tolist()[2]

    def get_count_of_tours(self):
        tournament_data = pd.read_excel(self.file_path, sheet_name="Турнирные данные")
        return tournament_data[tournament_data.columns[1]].tolist()[3]

    def get_current_tour(self):
        tournament_data = pd.read_excel(self.file_path, sheet_name="Турнирные данные")
        return tournament_data[tournament_data.columns[1]].tolist()[4]

    def set_current_tour(self, ct):
        data = self.get_data()
        tournament_data = pd.DataFrame({"Название турнира:": [data[0]],
                                        "ФИО судьи:": [data[1]],
                                        "ФИО помощника судьи:": [data[2]],
                                        "Система проведения соревнований:": [data[3]],
                                        "Количество туров:": [data[4]],
                                        "Номер текущего тура": ct,
                                        "Дата начала соревнований:": [data[6]],
                                        "Дата окончания соревнований:": [data[7]],
                                        "Приоритет 1 при равенстве очков:": [data[8]],
                                        "Приоритет 2 при равенстве очков:": [data[9]],
                                        "Приоритет 3 при равенстве очков:": [data[10]],
                                        "Приоритет 4 при равенстве очков:": [data[11]]}).T

        writer = pd.ExcelWriter(self.file_path, engine="openpyxl", mode="a", if_sheet_exists='replace')
        tournament_data.to_excel(writer, sheet_name="Турнирные данные", index=True, header=False)

        writer.close()

    def get_date_of_start(self):
        tournament_data = pd.read_excel(self.file_path, sheet_name="Турнирные данные")
        return tournament_data[tournament_data.columns[1]].tolist()[5]

    def get_date_of_end(self):
        tournament_data = pd.read_excel(self.file_path, sheet_name="Турнирные данные")
        return tournament_data[tournament_data.columns[1]].tolist()[6]

    def get_priority_1(self):
        tournament_data = pd.read_excel(self.file_path, sheet_name="Турнирные данные")
        return tournament_data[tournament_data.columns[1]].tolist()[7]

    def get_priority_2(self):
        tournament_data = pd.read_excel(self.file_path, sheet_name="Турнирные данные")
        return tournament_data[tournament_data.columns[1]].tolist()[8]

    def get_priority_3(self):
        tournament_data = pd.read_excel(self.file_path, sheet_name="Турнирные данные")
        return tournament_data[tournament_data.columns[1]].tolist()[9]

    def get_priority_4(self):
        tournament_data = pd.read_excel(self.file_path, sheet_name="Турнирные данные")
        return tournament_data[tournament_data.columns[1]].tolist()[10]

    def get_data(self):
        tournament_data = pd.read_excel(self.file_path, sheet_name="Турнирные данные")
        tn_name = tournament_data.columns[1]
        data = tournament_data[tournament_data.columns[1]].tolist()
        data.insert(0, tn_name)
        return data

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

        # Пересортировываем игроков в порядке их номеров
        self.players.sort(key=lambda x: x.number)

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
                        list_of_opponents = [i[0] for i in first_player.list_of_opponents]
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

        while len(pairs) * 2 != len(self.players):
            # Список возможных пар имеет вид: [(player_1, player_2), (player_3, player_4), ...]
            list_of_possible_pairs = []

            # Список игроков с количеством возможных
            # оппонентов из последней группы вида:
            # [[player_1, count_of_opponents], [player_2, count_of_opponents], ...]
            counts_of_possible_opponents = []

            # Удаляем из итогового списка пар те пары, которые
            # были составлены из игроков последней группы, а
            # также составляем список всех рёбер
            # (возможных пар) последней группы и заполняем
            # counts_of_possible_opponents
            for player in groups[-1]:
                # Второй параметр None необходим, чтобы не выбрасывалось исключение
                pairs.pop(player, None)
                list_of_opponents = [i[0] for i in player.list_of_opponents]
                counts_of_possible_opponents.append([player, 0])
                for player_2 in groups[-1]:
                    if player_2 not in list_of_opponents \
                            and player_2 != player \
                            and [player, player_2] not in list_of_possible_pairs:
                        list_of_possible_pairs.append((player, player_2))
                        counts_of_possible_opponents[-1][1] += 1

            # Также расформировываем последнюю группу, так как в случае,
            # если мы не сможем распределить пары, придется
            # расформировывать уже 2 группы и так далее
            groups[-2] = groups[-2] + groups[-1]
            groups.pop(-1)

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
                    if (pair[0] == player or pair[1] == player) and distributed_players.count(pair[0]) == 0 \
                            and distributed_players.count(pair[1]) == 0:
                        if pair[0].get_count_of_white_games() >= pair[1].get_count_of_white_games():
                            pairs[pair[1]] = pair[0]
                        else:
                            pairs[pair[0]] = pair[1]
                        distributed_players.append(pair[0])
                        distributed_players.append(pair[1])

        return pairs
