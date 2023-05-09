import tkinter as tk
import tournament_and_results_table as tart
import participant_entry_page as pep


class ToursFrame(tk.Frame):
    players = []

    def __init__(self, parent: tk.Tk, tn: tart.Tournament):
        tk.Frame.__init__(self, parent, background="#FFFFFF")
        self.parent = parent
        self.tn = tn
        self.create_elements()
        self.pack(expand=1)

    def create_prev_frame(self):
        if self.tn.current_tour == 1:
            [child.destroy() for child in self.parent.winfo_children()]
            pep.ParticipantsFrame(parent=self.parent, tn=self.tn)

    def next_tour(self, results):
        self.tn.current_tour += 1
        dict_results = {}
        for white_player, white_player_result, black_player_result, black_player in results:
            dict_results[white_player] = int(white_player_result.get())
            dict_results[black_player] = int(black_player_result.get())

            white_player.number_of_points += int(white_player_result.get())
            black_player.number_of_points += int(black_player_result.get())

            white_player.list_of_opponents.append((black_player, int(white_player_result.get())))
            black_player.list_of_opponents.append((white_player, int(black_player_result.get())))

        [child.destroy() for child in self.parent.winfo_children()]
        ToursFrame(self.parent, self.tn)

    # width=950, height=400
    def create_pairs(self, frame: tk.Canvas):
        pairs_of_players = list(self.tn.draw().items())
        results = []
        label1 = tk.Label(text="№ стола", font=("Times New Roman", 14), background="#FFFFFF", width=8, anchor="center")
        label2 = tk.Label(text="ФИО участника", font=("Times New Roman", 14), background="#FFFFFF", width=14,
                          anchor="center")
        label3 = tk.Label(text="Результат", font=("Times New Roman", 14), background="#FFFFFF", width=10,
                          anchor="center")
        label4 = tk.Label(text="ФИО участника", font=("Times New Roman", 14), background="#FFFFFF", width=14,
                          anchor="center")
        frame.create_window(60, 30, window=label1)
        frame.create_window(280, 30, window=label2)
        frame.create_window(520, 30, window=label3)
        frame.create_window(760, 30, window=label4)

        for i in range(2, len(pairs_of_players) + 2):
            # Задаём номер стола
            number_of_table = tk.Label(text=f"{i - 1}.", font=("Times New Roman", 14), background="#FFFFFF", width=8,
                                       anchor="center")
            # ФИО игрока белым цветом
            white_color = tk.Label(text=f"{pairs_of_players[i - 2][0].name}", font=("Times New Roman", 14),
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
            # добавляем в результативный список подсписок следующего вида:
            # [игрок белыми, виджет для результата белых, виджет для результата черных, игрок черными]
            results.append((pairs_of_players[i - 2][0], white_result, black_result, pairs_of_players[i - 2][1]))

            # ФИО игрока черным цветом
            black_color = tk.Label(text=f"{pairs_of_players[i - 2][1].name}", font=("Times New Roman", 14),
                                   background="#FFFFFF",
                                   width=20,
                                   anchor="center")

            frame.create_window(60, i * 30, window=number_of_table)
            frame.create_window(280, i * 30, window=white_color)
            frame.create_window(500, i * 30, window=white_result)
            frame.create_window(540, i * 30, window=black_result)
            frame.create_window(760, i * 30, window=black_color)

        return results

    def create_elements(self):
        # fft - frame for text
        fft = tk.Frame(self,
                       background="#FFFFFF",
                       width=1000,
                       height=100
                       )
        fft.pack(expand=1, fill="both")
        # ffp - frame for participants
        ffp = tk.Frame(self,
                       background="#FFFFFF",
                       width=1000,
                       height=400
                       )
        ffp.pack(expand=1, fill="both")
        # ffb - frame for buttons
        ffb = tk.Frame(self,
                       background="#FFFFFF",
                       width=1000,
                       height=100
                       )
        ffb.pack(expand=1, fill="both")

        label0 = tk.Label(fft, text=f"Тур №{self.tn.current_tour}",
                          font=("Times New Roman", 36),
                          background="#FFFFFF",
                          width=36)
        label0.pack(expand=1, fill="both", pady=(0, 20))

        canvas = tk.Canvas(ffp, width=950, height=400, bg="#FFFFFF")
        results = self.create_pairs(canvas)
        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.pack(expand=1, side="left")

        scrollbar = tk.Scrollbar(ffp, orient="vertical")
        canvas["yscrollcommand"] = scrollbar.set
        scrollbar.config(command=canvas.yview)
        scrollbar.pack(anchor="sw", side="right", fill="y", padx=(5, 11))
        # self.bind("<MouseWheel>", lambda: on_canvas_scroll(canvas))

        button_back = tk.Button(ffb, text="Назад",
                                font=("Times New Roman", 14),
                                background="#FFFFFF",
                                width=20,
                                height=2,
                                relief="solid",
                                activebackground="#FFFFFF",
                                command=self.create_prev_frame
                                )
        button_back.grid(row=0, column=0, sticky="W", padx=(5, 25), pady=(10, 0))

        button_delete = tk.Button(ffb,
                                  text="Настройки",
                                  font=("Times New Roman", 14),
                                  background="#FFFFFF",
                                  width=20,
                                  height=2,
                                  relief="solid",
                                  activebackground="#FFFFFF"
                                  )
        button_delete.grid(row=0, column=1, sticky="W", padx=25, pady=(10, 0))

        button_add = tk.Button(ffb,
                               text="Просмотр таблицы",
                               font=("Times New Roman", 14),
                               background="#FFFFFF",
                               width=20,
                               height=2,
                               relief="solid",
                               activebackground="#FFFFFF"
                               )
        button_add.grid(row=0, column=2, sticky="W", padx=25, pady=(10, 0))

        button_next = tk.Button(ffb, text="Далее",
                                font=("Times New Roman", 14),
                                background="#FFFFFF",
                                width=20,
                                height=2,
                                relief="solid",
                                activebackground="#FFFFFF",
                                command=lambda: self.next_tour(results)
                                )
        button_next.grid(row=0, column=3, sticky="W", padx=(20, 10), pady=(10, 0))
