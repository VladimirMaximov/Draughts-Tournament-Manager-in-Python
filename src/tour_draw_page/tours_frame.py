import tkinter as tk
from tkinter import messagebox as mb
import copy

from tournament.tournament import Tournament
from tournament.table import TableFrame
import new_tournament_creation_page
import participant_entry_page.participants_frame as participants_frame
import pandas as pd


class MyFrame(tk.Frame):
    def __init__(self, frame, height, width=1000, *args, **kwargs):
        tk.Frame.__init__(self, frame, background="#FFFFFF", height=height, width=width, *args, **kwargs)


class ToursFrame(tk.Frame):

    def __init__(self, parent: tk.Tk, tn: Tournament):
        tk.Frame.__init__(self, parent, background="#FFFFFF")
        self.parent = parent
        self.tn = tn
        self.create_elements()
        self.pack(expand=1)

    def create_prev_frame(self):
        if self.tn.get_current_tour() == 1:
            [child.destroy() for child in self.parent.winfo_children()]
            participants_frame.ParticipantsFrame(parent=self.parent, tn=self.tn)
        else:
            [child.destroy() for child in self.parent.winfo_children()]
            # Функционал для возвращения на тур назад
            ToursFrame(parent=self.parent, tn=self.tn)

    @staticmethod
    def check_errors(results):
        for white_player, white_player_result, black_player_result, black_player in results:
            if white_player_result.get().isdigit() and black_player_result.get().isdigit():
                if int(white_player_result.get()) + int(black_player_result.get()) != 2:
                    mb.showwarning(title="Предупреждение",
                                   message=f"Проверьте результаты, возможно вы ввели некорректный исход партии. "
                                           f"Вернитесь на страницу назад и перепроверьте. "
                                           f"Возможные исходы:\n 2 : 0, 1 : 1, 0 : 2")
            else:
                mb.showerror(title="Ошибка",
                             message="Проверьте результаты, в полях ввода должны быть целые числа. "
                                     "Возможные исходы:\n 2 : 0, 1 : 1, 0 : 2")
                return True
        return False

    def next_tour(self, results):
        # Проверяем результат на ошибки
        if self.check_errors(results):
            return

        for white_player, white_player_result, black_player_result, black_player in results:

            # Так как мы можем много раз вызывать итоговую таблицу,
            # то обновления информации об игроках может выполняться
            # несколько раз, поэтому требуется делать проверку

            white_player.number_of_points += int(white_player_result.get())
            black_player.number_of_points += int(black_player_result.get())

            white_player.list_of_opponents.append((black_player, "w", int(white_player_result.get())))
            black_player.list_of_opponents.append((white_player, "b", int(black_player_result.get())))

        # Распределяем места
        self.tn.prize_distribution()

        self.tn.fill_tour()
        self.tn.fill_tours_sheet()

        # Если это был последний тур, то вместо
        # жеребьевки следующего тура выдаем таблицу
        if int(self.tn.get_current_tour()) >= int(self.tn.get_count_of_tours()):
            [child.destroy() for child in self.parent.winfo_children()]
            TableFrame(self.parent, self.tn)
        else:
            self.tn.set_current_tour(self.tn.get_current_tour() + 1)
            [child.destroy() for child in self.parent.winfo_children()]
            ToursFrame(self.parent, self.tn)

    # def change_settings(self):
    #     window1 = tk.Tk()
    #     tn = copy.deepcopy(self.tn)
    #     new_tournament_creation_page.ParametersFrame(parent=window1, tn=tn)
    #     window1.mainloop()

    # width=950, height=400
    def create_pairs(self, canvas: tk.Canvas):
        # Пары игроков представлены списком кортежей их двух элементов,
        # где первый элемент - игрок белым цветом, второй элемент - игрок черным цветом.
        # Дополнительно может быть третий и четвертый элемент - результат белых и черных
        # соответственно, это необходимо, чтобы изначально
        # задать объекты entry при "возвращении назад"
        pairs_of_players = []
        if True:
            pairs_of_players = list(self.tn.draw().items())
        # else:
        #     # Если мы вернулись назад, то первым делом мы должны
        #     # для каждого игрока изменить его количество очков и
        #     # количество побед, но пока не удалять последнего противника,
        #     # так как он нам пригодится для составления списка пар
        #     for player in self.tn.players:
        #         last_opponent = player.list_of_opponents[-1]
        #         player.number_of_points -= last_opponent[1]
        #         if last_opponent[1] == 2:
        #             player.number_of_wins -= 1
        #     # Сортируем игроков так, чтобы результат получился такой же,
        #     # как и был на предыдущем туре, так как количество очков и
        #     # побед мы уже уменьшили, то осталось только посчитать правильно
        #     # коэффициенты, без участия последнего игрока (так как мы
        #     # его ещё не удалили из списка оппонентов)
        #     self.tn.sort_players(self.go_back)
        #     for player in self.tn.players:
        #         if len(player.list_of_opponents) == self.tn.current_tour:
        #             # В данном случае:
        #             # opponent[0] - текущий оппонент игрока,
        #             # opponent[1] - результат с этим оппонентом,
        #             # opponent[2] - цвет, которым играл текущий игрок (а не его оппонент)
        #             opponent = player.list_of_opponents.pop()
        #             player_with_res = opponent[0].list_of_opponents.pop()
        #             if opponent[2] == "w":
        #                 pairs_of_players.append((player_with_res[0], opponent[0], opponent[1], player_with_res[1]))
        #             else:
        #                 pairs_of_players.append((opponent[0], player_with_res[0], player_with_res[1], opponent[1]))
        # Результат представлен списком кортежей,
        # состоящих из 4 элементов:
        # [Игрок белым цветом;
        # объект entry, хранящий результат белых;
        # объект entry, хранящий результат черных;
        # игрок черным цветом]
        results = []
        label1 = tk.Label(text="№ стола", font=("Times New Roman", 14), background="#FFFFFF", width=8, anchor="center")
        label2 = tk.Label(text="ФИО участника", font=("Times New Roman", 14), background="#FFFFFF", width=14,
                          anchor="center")
        label3 = tk.Label(text="Результат", font=("Times New Roman", 14), background="#FFFFFF", width=10,
                          anchor="center")
        label4 = tk.Label(text="ФИО участника", font=("Times New Roman", 14), background="#FFFFFF", width=14,
                          anchor="center")
        canvas.create_window(60, 30, window=label1)
        canvas.create_window(280, 30, window=label2)
        canvas.create_window(520, 30, window=label3)
        canvas.create_window(760, 30, window=label4)

        for i in range(len(pairs_of_players)):
            # Задаём номер стола
            number_of_table = tk.Label(text=f"{i + 1}.", font=("Times New Roman", 14), background="#FFFFFF", width=8,
                                       anchor="center")
            # ФИО игрока белым цветом
            white_color = tk.Label(text=f"{pairs_of_players[i][0].name}", font=("Times New Roman", 14),
                                   background="#FFFFFF",
                                   width=20,
                                   anchor="center")

            # Виджет для результата белых
            white_result_var = tk.StringVar()
            white_result = tk.Entry(font=("Times New Roman", 14), background="#E8E8E8", relief="flat", width=3,
                                    textvariable=white_result_var)
            # Виджет для результата черных
            black_result_var = tk.StringVar()
            black_result = tk.Entry(font=("Times New Roman", 14), background="#E8E8E8", relief="flat", width=3,
                                    textvariable=black_result_var)
            # Если мы вернулись, то задаём
            # результат белых и черных
            # if self.go_back:
            #     white_result.insert(0, pairs_of_players[i][2])
            #     black_result.insert(0, pairs_of_players[i][3])
            # добавляем в результативный список подсписок следующего вида:
            # [игрок белыми, виджет для результата белых, виджет для результата черных, игрок черными]
            results.append((pairs_of_players[i][0], white_result, black_result, pairs_of_players[i][1]))

            # ФИО игрока черным цветом
            black_color = tk.Label(text=f"{pairs_of_players[i][1].name}", font=("Times New Roman", 14),
                                   background="#FFFFFF",
                                   width=20,
                                   anchor="center")

            canvas.create_window(60, (i + 2) * 30, window=number_of_table)
            canvas.create_window(280, (i + 2) * 30, window=white_color)
            canvas.create_window(500, (i + 2) * 30, window=white_result)
            canvas.create_window(540, (i + 2) * 30, window=black_result)
            canvas.create_window(760, (i + 2) * 30, window=black_color)

        return results

    def create_elements(self):

        frame_for_text = MyFrame(self.parent, height=100)
        frame_for_text.pack(expand=1, fill="both")

        frame_for_participants = MyFrame(self.parent, height=400)
        frame_for_participants.pack(expand=1, fill="both")

        frame_for_buttons = MyFrame(self.parent, height=100)
        frame_for_buttons.pack(expand=1, fill="both")

        label0 = tk.Label(frame_for_text, text=f"Тур №{self.tn.get_current_tour()}",
                          font=("Times New Roman", 36),
                          background="#FFFFFF",
                          width=36)
        label0.pack(expand=1, fill="both", pady=(0, 20))

        canvas = tk.Canvas(frame_for_participants, width=950, height=400, bg="#FFFFFF")
        results = self.create_pairs(canvas)
        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.pack(expand=1, side="left")

        scrollbar = tk.Scrollbar(frame_for_participants, orient="vertical")
        canvas["yscrollcommand"] = scrollbar.set
        scrollbar.config(command=canvas.yview)
        scrollbar.pack(anchor="sw", side="right", fill="y", padx=(5, 11))
        # self.bind("<MouseWheel>", lambda: on_canvas_scroll(canvas))

        button_back = tk.Button(frame_for_buttons, text="Назад",
                                font=("Times New Roman", 14),
                                background="#FFFFFF",
                                width=20,
                                height=2,
                                relief="solid",
                                activebackground="#FFFFFF",
                                command=self.create_prev_frame
                                )
        button_back.grid(row=0, column=0, sticky="W", padx=(5, 25), pady=(10, 0))

        button_delete = tk.Button(frame_for_buttons,
                                  text="Настройки",
                                  font=("Times New Roman", 14),
                                  background="#FFFFFF",
                                  width=20,
                                  height=2,
                                  relief="solid",
                                  activebackground="#FFFFFF",
                                  #command=self.change_settings
                                  )
        button_delete.grid(row=0, column=1, sticky="W", padx=25, pady=(10, 0))

        button_add = tk.Button(frame_for_buttons,
                               text="Просмотр таблицы",
                               font=("Times New Roman", 14),
                               background="#FFFFFF",
                               width=20,
                               height=2,
                               relief="solid",
                               activebackground="#FFFFFF"
                               )
        button_add.grid(row=0, column=2, sticky="W", padx=25, pady=(10, 0))

        text = f"Жеребьевка тура №{self.tn.get_current_tour() + 1}"
        if self.tn.get_current_tour() == self.tn.get_count_of_tours():
            text = "Итоговая таблица"

        button_next = tk.Button(frame_for_buttons, text=text,
                                font=("Times New Roman", 14),
                                background="#FFFFFF",
                                width=20,
                                height=2,
                                relief="solid",
                                activebackground="#FFFFFF",
                                command=lambda: self.next_tour(results)
                                )
        button_next.grid(row=0, column=3, sticky="W", padx=(20, 10), pady=(10, 0))
