import tkinter as tk
import tournament_and_results_table as tart


class TableFrame(tk.Frame):

    def __init__(self, parent: tk.Tk, tn: tart.Tournament):
        tk.Frame.__init__(self, parent, background="#FFFFFF")
        self.parent = parent
        self.tn = tn
        self.set_window()
        self.create_elements()
        self.pack(expand=1)

    def set_window(self):
        width = 1000
        height = 600
        self.parent.title("Турнирная таблица")
        self.parent.config(bg="#FFFFFF")

        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()

        x = (screen_width - width) / 2
        y = (screen_height - height) / 2

        self.parent.geometry(f"{width}x{height}+{int(x)}+{int(y)}")

    def create_table(self, canvas_frame: tk.Canvas):
        label1 = tk.Label(canvas_frame, text="ФИО участника", font=("Times New Roman", 14), background="#FFFFFF", width=20, anchor="center")
        label2 = tk.Label(canvas_frame, text="Пр. 1", font=("Times New Roman", 14), background="#FFFFFF", width=5, anchor="center")
        label3 = tk.Label(canvas_frame, text="Пр. 2", font=("Times New Roman", 14), background="#FFFFFF", width=5, anchor="center")
        label4 = tk.Label(canvas_frame, text="Пр. 3", font=("Times New Roman", 14), background="#FFFFFF", width=5, anchor="center")
        label5 = tk.Label(canvas_frame, text="Пр. 4", font=("Times New Roman", 14), background="#FFFFFF", width=5, anchor="center")
        label6 = tk.Label(canvas_frame, text="Кол-во очков", font=("Times New Roman", 14), background="#FFFFFF", width=11, anchor="center")
        label7 = tk.Label(canvas_frame, text="Место", font=("Times New Roman", 14), background="#FFFFFF", width=5, anchor="center")
        canvas_frame.create_window(300, 30, window=label1)
        canvas_frame.create_window(500, 30, window=label2)
        canvas_frame.create_window(600, 30, window=label3)
        canvas_frame.create_window(700, 30, window=label4)
        canvas_frame.create_window(800, 30, window=label5)
        canvas_frame.create_window(950, 30, window=label6)
        canvas_frame.create_window(1100, 30, window=label7)

        for i in range(len(self.tn.players)):
            label1 = tk.Label(canvas_frame, text=f"{self.tn.players[i].name}", font=("Times New Roman", 14), background="#FFFFFF",
                              width=20, anchor="center")
            if self.tn.priority_1 == "Дополнительный матч":
                pr_1 = "Д. м."
            elif self.tn.priority_1 == "Результат личной встречи":
                pr_1 = "Л. в."
            elif self.tn.priority_1 == "Наибольшее число побед":
                pr_1 = self.tn.players[i].number_of_wins
            elif self.tn.priority_1 == "Система коэффициентов Шмульяна":
                pr_1 = self.tn.players[i].schmullan_coefficient
            else:
                pr_1 = self.tn.players[i].buchholz_coefficient
            label2 = tk.Label(canvas_frame, text=f"{pr_1}", font=("Times New Roman", 14), background="#FFFFFF", width=5,
                              anchor="center")
            if self.tn.priority_2 == "Дополнительный матч":
                pr_1 = "Д. м."
            elif self.tn.priority_2 == "Результат личной встречи":
                pr_1 = "Л. в."
            elif self.tn.priority_2 == "Наибольшее число побед":
                pr_1 = self.tn.players[i].number_of_wins
            elif self.tn.priority_2 == "Система коэффициентов Шмульяна":
                pr_1 = self.tn.players[i].schmullan_coefficient
            else:
                pr_1 = self.tn.players[i].buchholz_coefficient
            label3 = tk.Label(canvas_frame, text=f"{pr_1}", font=("Times New Roman", 14), background="#FFFFFF", width=5,
                              anchor="center")
            if self.tn.priority_3 == "Дополнительный матч":
                pr_1 = "Д. м."
            elif self.tn.priority_3 == "Результат личной встречи":
                pr_1 = "Л. в."
            elif self.tn.priority_3 == "Наибольшее число побед":
                pr_1 = self.tn.players[i].number_of_wins
            elif self.tn.priority_3 == "Система коэффициентов Шмульяна":
                pr_1 = self.tn.players[i].schmullan_coefficient
            else:
                pr_1 = self.tn.players[i].buchholz_coefficient
            label4 = tk.Label(canvas_frame, text=f"{pr_1}", font=("Times New Roman", 14), background="#FFFFFF", width=5,
                              anchor="center")
            if self.tn.priority_4 == "Дополнительный матч":
                pr_1 = "Д. м."
            elif self.tn.priority_4 == "Результат личной встречи":
                pr_1 = "Л. в."
            elif self.tn.priority_4 == "Наибольшее число побед":
                pr_1 = self.tn.players[i].number_of_wins
            elif self.tn.priority_4 == "Система коэффициентов Шмульяна":
                pr_1 = self.tn.players[i].schmullan_coefficient
            else:
                pr_1 = self.tn.players[i].buchholz_coefficient
            label5 = tk.Label(canvas_frame, text=f"{pr_1}", font=("Times New Roman", 14), background="#FFFFFF", width=5,
                              anchor="center")
            label6 = tk.Label(canvas_frame, text=f"{self.tn.players[i].number_of_points}", font=("Times New Roman", 14), background="#FFFFFF",
                              width=11, anchor="center")
            label7 = tk.Label(canvas_frame, text=f"{i + 1}", font=("Times New Roman", 14), background="#FFFFFF", width=5,
                              anchor="center")

            canvas_frame.create_window(300, 30*(i + 2), window=label1)
            canvas_frame.create_window(500, 30*(i + 2), window=label2)
            canvas_frame.create_window(600, 30*(i + 2), window=label3)
            canvas_frame.create_window(700, 30*(i + 2), window=label4)
            canvas_frame.create_window(800, 30*(i + 2), window=label5)
            canvas_frame.create_window(950, 30*(i + 2), window=label6)
            canvas_frame.create_window(1100, 30*(i + 2), window=label7)

    def create_elements(self):
        # ФИО, игры, результат
        # fft - frame for text
        fft = tk.Frame(self,
                       background="#FFFFFF",
                       width=1000,
                       height=100
                       )
        fft.pack(expand=1, fill="both")
        # fftt - frame for tournament table
        fftt = tk.Frame(self,
                        background="#FFFFFF",
                        width=1000,
                        height=450
                        )
        fftt.pack(expand=1, fill="both")

        label0 = tk.Label(fft, text=f"Турнирная таблица на {self.tn.current_tour} тур.",
                          font=("Times New Roman", 36),
                          background="#FFFFFF",
                          width=36)
        label0.pack(expand=1, fill="both", pady=(0, 20))

        canvas_frame = tk.Canvas(fftt, width=950, height=400, bg="#FFFFFF")
        self.create_table(canvas_frame)
        canvas_frame.update_idletasks()
        canvas_frame.configure(scrollregion=canvas_frame.bbox("all"))
        canvas_frame.pack(expand=1, side="left")

        scrollbar = tk.Scrollbar(fftt, orient="vertical")
        canvas_frame["yscrollcommand"] = scrollbar.set
        scrollbar.config(command=canvas_frame.yview)
        scrollbar.pack(anchor="sw", side="right", fill="y", padx=(5, 11))
