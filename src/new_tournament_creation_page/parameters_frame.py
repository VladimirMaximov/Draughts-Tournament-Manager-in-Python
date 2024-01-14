import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog as fd
import start_page
import tournament_and_results_table as tournament
import participant_entry_page
from tkcalendar import Calendar, DateEntry


class MyLabels(tk.Label):
    def __init__(self, frame, text, *args, **kwargs):
        tk.Label.__init__(self,
                          frame,
                          text=text,
                          font=("Times New Roman", 14),
                          background="#FFFFFF",
                          *args, **kwargs
                          )


class MyEntry(tk.Entry):
    def __init__(self, frame, *args, **kwargs):
        tk.Entry.__init__(self,
                          frame,
                          font=("Times New Roman", 14),
                          background="#FFFFFF",
                          relief="solid",
                          width=69,
                          *args, **kwargs
                          )

class MyButton(tk.Button):
    def __init__(self, frame, *args, **kwargs):
        tk.Button.__init__(self,
                           frame,
                           font=("Times New Roman", 14),
                           background="#FFFFFF",
                           relief="solid",
                           activebackground="#E8E8E8",
                           *args, **kwargs)

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

        label_tn_name = MyLabels(frame_for_labels, text="Название турнира:")
        label_tn_name.pack()

        entry_tn_name = MyEntry(frame_for_settings)
        entry_tn_name.pack()

        label_path = MyLabels(frame_for_labels, text="Папка для сохранения турнира:")
        label_path.pack()

        button_select_path = MyButton(frame_for_settings, text="Выбрать папку для сохранения")
        button_select_path.pack()

        label_referee_name = MyLabels(frame_for_labels, text="ФИО судьи:")
        label_referee_name.pack()

        entry_referee_name = MyEntry(frame_for_settings)
        entry_referee_name.pack()

        label_assistant_referee_name = MyLabels(frame_for_labels, text="ФИО помощника судьи:")
        label_assistant_referee_name.pack()

        entry_assistant_referee_name = MyEntry(frame_for_settings)
        entry_assistant_referee_name.pack()

        label_system = MyLabels(frame_for_labels, text="Система проведения соревнований:")
        label_system.pack()

        system = ["Швейцарская система", "Олимпийская система", "Круговая система"]
        field = tk.StringVar()
        entry_system = MyCombobox(frame_for_settings, values=system, textvariable=field)
        entry_system.pack()

        label_count_of_tours = MyLabels(frame_for_labels, text="Количество туров:")
        label_count_of_tours.pack()

        entry_count_of_tours = MyEntry(frame_for_settings)
        entry_count_of_tours.pack()

        label_date_of_start = MyLabels(frame_for_labels, text="Дата начала турнира:")
        label_date_of_start.pack()

        entry_date_of_start = DateEntry(frame_for_settings, selectmode="day", date_pattern="dd-mm-yyyy")
        entry_date_of_start.pack()

        label_date_of_end = MyLabels(frame_for_labels, text="Дата окончания турнира:")
        label_date_of_end.pack()

        entry_date_of_end = DateEntry(frame_for_settings, selectmode="day", date_pattern="dd-mm-yyyy")

        # Задаем дату окончания по умолчанию равную дате начала + неделя
        date = entry_date_of_start.get_date() + Calendar.timedelta(days=7)
        entry_date_of_end.set_date(date=date)

        entry_date_of_end.pack()

        label_priority_1 = MyLabels(frame_for_labels, text="Приоритет 1 при равенстве очков:")
        label_priority_1.pack()

        entry_priority_1 = tk.Entry(frame_for_settings)
        entry_priority_1.pack()

        label_priority_2 = MyLabels(frame_for_labels, text="Приоритет 2 при равенстве очков:")
        label_priority_2.pack()

        entry_priority_2 = tk.Entry(frame_for_settings)
        entry_priority_2.pack()

        label_priority_3 = MyLabels(frame_for_labels, text="Приоритет 3 при равенстве очков:")
        label_priority_3.pack()

        entry_priority_3 = tk.Entry(frame_for_settings)
        entry_priority_3.pack()

        label_priority_4 = MyLabels(frame_for_labels, text="Приоритет 4 при равенстве очков:")
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
