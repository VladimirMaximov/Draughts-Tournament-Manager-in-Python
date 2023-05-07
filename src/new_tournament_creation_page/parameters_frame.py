import tkinter as tk
from tkinter import ttk
import start_page
import tournament_and_results_table as tournament
import participant_entry_page


class MyLabels(tk.Label):
    def __init__(self, frame, text, row, column, *args, **kwargs):
        tk.Label.__init__(self,
                          frame,
                          text=text,
                          font=("Times New Roman", 14),
                          background="#FFFFFF",
                          *args, **kwargs
                          )
        self.grid(row=row, column=column, sticky="W", pady=5, padx=5)


class MyEntry(tk.Entry):
    def __init__(self, frame, *args, **kwargs):
        tk.Entry.__init__(self,
                          frame,
                          font=("Times New Roman", 14),
                          background="#E8E8E8",
                          relief="flat",
                          width=69,
                          *args, **kwargs
                          )


class MyCombobox(ttk.Combobox):
    def __init__(self, frame, values, textvariable, width=67, state="normal", *args,
                 **kwargs):
        ttk.Combobox.__init__(self,
                              frame,
                              font=("Times New Roman", 14),
                              background="#000000",
                              textvariable=textvariable,
                              width=width,
                              values=values,
                              state=state,
                              *args, **kwargs
                              )
        self.option_add('*TCombobox*Listbox.font', ("Times New Roman", 14))


class ParametersFrame(tk.Frame):

    def __init__(self, parent: tk.Tk, tn: tournament.Tournament = None):
        tk.Frame.__init__(self, parent, background="#FFFFFF")
        self.parent = parent
        if tn is None:
            self.tn = tournament.Tournament()
        else:
            self.tn = tn

        self.tournament_name = tk.StringVar(value=self.tn.tournament_name)
        self.referee_name = tk.StringVar(value=self.tn.referee_name)
        self.assistant_referee_name = tk.StringVar(value=self.tn.assistant_referee_name)
        self.date = tk.StringVar(value=self.tn.date)
        self.system = tk.StringVar(value=self.tn.system)
        self.count_of_tours = tk.StringVar(value=self.tn.count_of_tours)
        self.count_of_parties = tk.StringVar(value=self.tn.count_of_parties)
        self.priority_1 = tk.StringVar(value=self.tn.priority_1)
        self.priority_2 = tk.StringVar(value=self.tn.priority_2)
        self.priority_3 = tk.StringVar(value=self.tn.priority_3)
        self.priority_4 = tk.StringVar(value=self.tn.priority_4)

        self.create_elements()
        self.pack(expand=1)

    def create_start_page(self):
        [child.destroy() for child in self.parent.winfo_children()]
        start_page.StartFrame(self.parent)

    def create_participants_page(self):
        [child.destroy() for child in self.parent.winfo_children()]
        self.tn.tournament_name = self.tournament_name.get()
        self.tn.referee_name = self.referee_name.get()
        self.tn.assistant_referee_name = self.assistant_referee_name.get()
        self.tn.date = self.date.get()
        self.tn.system = self.system.get()
        self.tn.count_of_tours = self.count_of_tours.get()
        self.tn.count_of_parties = self.count_of_parties.get()
        self.tn.priority_1 = self.priority_1.get()
        self.tn.priority_2 = self.priority_2.get()
        self.tn.priority_3 = self.priority_3.get()
        self.tn.priority_4 = self.priority_4.get()
        participant_entry_page.ParticipantsFrame(self.parent, self.tn)

    def create_elements(self):
        # ffif - frame for input fields
        ffif = tk.Frame(self,
                        background="#FFFFFF",
                        width=1000,
                        height=500
                        )
        ffif.pack(expand=1, fill="both")

        # ffb - frame for buttons
        ffb = tk.Frame(self,
                       background="#FFFFFF",
                       width=1000,
                       height=100
                       )
        ffb.pack(expand=1, fill="both")

        label0 = tk.Label(ffif, text="Параметры турнира",
                          font=("Times New Roman", 36),
                          background="#FFFFFF",
                          width=36)
        label0.grid(row=0, column=0, pady=5, padx=10, columnspan=2)

        MyLabels(ffif, text="Введите название турнира: ", row=1, column=0)
        MyLabels(ffif, text="ФИО судьи: ", row=2, column=0)
        MyLabels(ffif, text="ФИО помощника судьи: ", row=3, column=0)
        MyLabels(ffif, text="Система проведения соревнований: ", row=4, column=0)
        MyLabels(ffif, text="Количество туров: ", row=5, column=0)
        MyLabels(ffif, text="Количество партий в игре: ", row=6, column=0)
        MyLabels(ffif, text="Дата проведения: ", row=7, column=0)
        MyLabels(ffif, text="Распределение мест при равенстве очков: ", row=8, column=0)

        entry1 = MyEntry(ffif, textvariable=self.tournament_name)
        entry1.grid(row=1, column=1, sticky="W", pady=5, padx=(5, 0))

        entry2 = MyEntry(ffif, textvariable=self.referee_name)
        entry2.grid(row=2, column=1, sticky="W", pady=5, padx=(5, 0))

        entry3 = MyEntry(ffif, textvariable=self.assistant_referee_name)
        entry3.grid(row=3, column=1, sticky="W", pady=5, padx=(5, 0))

        entry4 = MyEntry(ffif, textvariable=self.date)
        entry4.grid(row=7, column=1, sticky="W", pady=5, padx=(5, 0))

        combobox1_values = ["Круговая система", "Швейцарская система", "Олимпийская система"]
        combobox1 = MyCombobox(ffif, textvariable=self.system, values=combobox1_values,
                               state="readonly")
        combobox1.grid(row=4, column=1, sticky="W", pady=5, padx=5)

        combobox2_values = [str(x) for x in range(1, 20)]
        combobox2 = MyCombobox(ffif, textvariable=self.count_of_tours, values=combobox2_values)
        combobox2.grid(row=5, column=1, sticky="W", pady=5, padx=5)

        combobox3_values = ["1", "2"]
        combobox3 = MyCombobox(ffif, textvariable=self.count_of_parties, values=combobox3_values)
        combobox3.grid(row=6, column=1, sticky="W", pady=5, padx=5)

        MyLabels(ffif, text="Приоритет 1: ", row=8, column=1)
        MyLabels(ffif, text="Приоритет 2: ", row=9, column=1)
        MyLabels(ffif, text="Приоритет 3: ", row=10, column=1)
        MyLabels(ffif, text="Приоритет 4: ", row=11, column=1)

        prioritising = ["Дополнительный матч", "Результат личной встречи", "Наибольшее число побед",
                        "Система коэффициентов Шмульяна", "Система коэффициентов Бухгольца"]

        combobox4 = MyCombobox(ffif, values=prioritising, textvariable=self.priority_1, width=53, state="readonly")
        combobox4.grid(row=8, column=1, sticky="W", pady=5, padx=(131, 0))

        combobox5 = MyCombobox(ffif, values=prioritising, textvariable=self.priority_2, width=53, state="readonly")
        combobox5.grid(row=9, column=1, sticky="W", pady=5, padx=(131, 0))

        combobox6 = MyCombobox(ffif, values=prioritising, textvariable=self.priority_3, width=53, state="readonly")
        combobox6.grid(row=10, column=1, sticky="W", pady=5, padx=(131, 0))

        combobox7 = MyCombobox(ffif, values=prioritising, textvariable=self.priority_4, width=53, state="readonly")
        combobox7.grid(row=11, column=1, sticky="W", pady=5, padx=(131, 0))

        # entry1.insert(0, self.tournament_name)
        # entry2.insert(0, self.referee_name)
        # entry3.insert(0, self.assistant_referee_name)
        # entry4.insert(0, self.date)
        # combobox1.set(self.system)
        # combobox2.set(self.count_of_tours)
        # combobox3.set(self.count_of_parties)
        # combobox4.set(self.priority_1)
        # combobox5.set(self.priority_2)
        # combobox6.set(self.priority_3)
        # combobox7.set(self.priority_4)

        button_back = tk.Button(ffb, text="Назад",
                                font=("Times New Roman", 14),
                                background="#FFFFFF",
                                width=20,
                                height=2,
                                relief="solid",
                                activebackground="#FFFFFF",
                                command=self.create_start_page
                                )
        button_back.grid(row=0, column=0, sticky="W", padx=5, pady=5)

        button_next = tk.Button(ffb, text="Далее",
                                font=("Times New Roman", 14),
                                background="#FFFFFF",
                                width=20,
                                height=2,
                                relief="solid",
                                activebackground="#FFFFFF",
                                command=self.create_participants_page
                                )
        button_next.grid(row=0, column=1, sticky="W", padx=(560, 5), pady=5)
