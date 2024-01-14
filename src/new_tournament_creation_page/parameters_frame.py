import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog as fd
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

        self.create_elements(tn)
        self.pack(expand=1)

    def create_start_page(self):
        [child.destroy() for child in self.parent.winfo_children()]
        start_page.StartFrame(self.parent)

    def create_participants_page(self):

        self.tn.count_of_tours = int(self.tn.count_of_tours)
        self.tn.count_of_parties = int(self.tn.count_of_parties)

        [child.destroy() for child in self.parent.winfo_children()]
        participant_entry_page.ParticipantsFrame(self.parent, self.tn)

    def create_elements(self, tn):

        # Фрейм для названия раздела
        frame_for_title = tk.Frame(self.parent)
        frame_for_title.pack()

        # Фрейм для ввода всех настроек
        frame_for_settings = tk.Frame(self.parent)
        frame_for_settings.pack()

        # Фрейм для названий полей ввода
        frame_for_labels = tk.Frame(frame_for_settings)
        frame_for_labels.pack(side="left")

        # Фрейм для полей ввода
        frame_for_data = tk.Frame(frame_for_settings)
        frame_for_data.pack(side="right")

        label_tn_name = tk.Label(frame_for_labels, text="Название турнира:")
        label_tn_name.pack()

        entry_tn_name = tk.Entry(frame_for_settings)
        entry_tn_name.pack()

        label_path = tk.Label(frame_for_labels, text="")
        label_path.pack()

        button

        label_referee_name = tk.Label(frame_for_labels, text="ФИО судьи:")
        label_referee_name.pack()

        entry_referee_name = tk.Entry(frame_for_settings)
        entry_referee_name.pack()

        label_assistant_referee_name = tk.Label(frame_for_labels, text="ФИО помощника судьи:")
        label_assistant_referee_name.pack()

        entry_assistant_referee_name = tk.Entry(frame_for_settings)
        entry_assistant_referee_name.pack()

        label_system = tk.Label(frame_for_labels, text="Система проведения соревнований:")
        label_system.pack()

        entry_system = tk.Entry(frame_for_settings)
        entry_system.pack()

        label_count_of_tours = tk.Label(frame_for_labels, text="Количество туров:")
        label_count_of_tours.pack()

        entry_count_of_tours = tk.Entry(frame_for_settings)
        entry_count_of_tours.pack()

        label_current_tour = tk.Label(frame_for_labels, text="Номер текущего тура:")
        label_current_tour.pack()

        entry_current_tour = tk.Entry(frame_for_settings)
        entry_current_tour.pack()

        label_date_of_start = tk.Label(frame_for_labels, text="Дата начала турнира:")
        label_date_of_start.pack()

        entry_date_of_start = tk.Entry(frame_for_settings)
        entry_date_of_start.pack()

        label_date_of_end = tk.Label(frame_for_labels, text="Дата окончания турнира:")
        label_date_of_end.pack()

        entry_date_of_end = tk.Entry(frame_for_settings)
        entry_date_of_end.pack()

        label_priority_1 = tk.Label(frame_for_labels, text="Приоритет 1 при равенстве очков:")
        label_priority_1.pack()

        entry_priority_1 = tk.Entry(frame_for_settings)
        entry_priority_1.pack()

        label_priority_2 = tk.Label(frame_for_labels, text="Приоритет 2 при равенстве очков:")
        label_priority_2.pack()

        entry_priority_2 = tk.Entry(frame_for_settings)
        entry_priority_2.pack()

        label_priority_3 = tk.Label(frame_for_labels, text="Приоритет 3 при равенстве очков:")
        label_priority_3.pack()

        entry_priority_3 = tk.Entry(frame_for_settings)
        entry_priority_3.pack()

        label_priority_4 = tk.Label(frame_for_labels, text="Приоритет 4 при равенстве очков:")
        label_priority_4.pack()

        entry_priority_4 = tk.Entry(frame_for_settings)
        entry_priority_4.pack()


    def set_window(self):
        width = 1000
        height = 600
        self.parent.title("Настройки")
        self.parent.configure(background="#FFFFFF")

        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()

        x = (screen_width - width) / 2
        y = (screen_height - height) / 2

        self.parent.geometry(f"{width}x{height}+{int(x)}+{int(y)}")
