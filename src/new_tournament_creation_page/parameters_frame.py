import datetime
import os
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog as fd
import start_page
import tournament.tournament as tournament
import participant_entry_page
from tkcalendar import Calendar, DateEntry
import pandas as pd


class MyLabels(tk.Label):
    def __init__(self, frame, text, *args, font=("Times New Roman", 14), **kwargs):
        tk.Label.__init__(self,
                          frame,
                          text=text,
                          font=font,
                          background="#FFFFFF",
                          width=32,
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
    def __init__(self, frame, font=("Times New Roman", 10), width=88, *args, **kwargs):
        tk.Button.__init__(self,
                           frame,
                           font=font,
                           background="#FFFFFF",
                           relief="solid",
                           width=width,
                           activebackground="#E8E8E8",
                           *args, **kwargs)


class MyCombobox(ttk.Combobox):
    def __init__(self, frame, values, textvariable=None, width=67, state="normal", *args,
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

    def __init__(self, parent: tk.Tk, tn: tournament.Tournament = tournament.Tournament()):
        tk.Frame.__init__(self, parent, background="#FFFFFF")
        self.parent = parent
        self.tn = tn
        self.create_elements()
        self.pack(expand=1)

    def create_start_page(self):
        [child.destroy() for child in self.parent.winfo_children()]
        start_page.StartFrame(self.parent)

    def create_participants_page(self):

        [child.destroy() for child in self.parent.winfo_children()]
        participant_entry_page.ParticipantsFrame(self.parent, self.tn)

    @staticmethod
    def create_path_to_file(path_to_directory, tournament_name, date_start: datetime.date):
        return path_to_directory + "/" + tournament_name + " " + str(date_start) + ".xlsx"


    def create_excel_file(self, data):
        # data = [name_of_tn, referee_name, assistant_referee_name, system,
        # count_of_tours, date_of_start, date_of_end,
        # priority_1, priority_2, priority_3, priority_4]

        # Базовая таблица пустая, так как ещё не внесены игроки
        base_table = pd.DataFrame()

        # Турнирные данные вносим и транспонируем для читаемости
        tournament_data = pd.DataFrame({"Название турнира:": [data[0]],
                                        "ФИО судьи:": [data[1]],
                                        "ФИО помощника судьи:": [data[2]],
                                        "Система проведения соревнований:": [data[3]],
                                        "Количество туров:": [data[4]],
                                        "Номер текущего тура": 1,
                                        "Дата начала соревнований:": [data[5]],
                                        "Дата окончания соревнований:": [data[6]],
                                        "Приоритет 1 при равенстве очков:": [data[7]],
                                        "Приоритет 2 при равенстве очков:": [data[8]],
                                        "Приоритет 3 при равенстве очков:": [data[9]],
                                        "Приоритет 4 при равенстве очков:": [data[10]]}).T

        # Туры пустые, так как ещё не внесены игроки и не проведено ни одного тура
        tours = pd.DataFrame()

        # Словарь названий таблиц и самих таблиц
        sheets = {"Основная таблица": base_table, "Турнирные данные": tournament_data, "Туры": tours}

        writer = pd.ExcelWriter(self.tn.file_path, engine="xlsxwriter")

        for sheet_name in sheets.keys():
            sheets[sheet_name].to_excel(writer, sheet_name=sheet_name, index=True, header=False)

        writer.close()

    def change_excel_file(self, data, current_tour):
        # data = [name_of_tn, referee_name, assistant_referee_name, system,
        # count_of_tours, date_of_start, date_of_end,
        # priority_1, priority_2, priority_3, priority_4]
        tournament_data = pd.DataFrame({"Название турнира:": [data[0]],
                                        "ФИО судьи:": [data[1]],
                                        "ФИО помощника судьи:": [data[2]],
                                        "Система проведения соревнований:": [data[3]],
                                        "Количество туров:": [data[4]],
                                        "Номер текущего тура": current_tour,
                                        "Дата начала соревнований:": [data[5]],
                                        "Дата окончания соревнований:": [data[6]],
                                        "Приоритет 1 при равенстве очков:": [data[7]],
                                        "Приоритет 2 при равенстве очков:": [data[8]],
                                        "Приоритет 3 при равенстве очков:": [data[9]],
                                        "Приоритет 4 при равенстве очков:": [data[10]]}).T

        # Путь до папки с файлом
        directory_path = self.tn.file_path[: self.tn.file_path.rindex("/")]

        # Переименовываем файл, так как пользователь мог изменить дату или название турнира
        os.rename(self.tn.file_path, self.create_path_to_file(directory_path, data[0], data[5]))

        # Теперь переписываем путь к файлу
        self.tn.file_path = self.create_path_to_file(directory_path, data[0], data[5])

        # После чего уже заполняем новые данные
        writer = pd.ExcelWriter(self.tn.file_path, engine="openpyxl", mode="a", if_sheet_exists='replace')
        tournament_data.to_excel(writer, sheet_name="Турнирные данные", index=True, header=False)

        writer.close()

    def create_elements(self):

        # Фрейм для названия раздела
        frame_for_title = tk.Frame(self.parent, background="#FFFFFF")
        frame_for_title.pack(pady=5)

        label_title = MyLabels(frame_for_title, text="Параметры турнира", font=("Times New Roman", 32))
        label_title.pack()

        # Фрейм для ввода всех настроек
        frame_for_settings = tk.Frame(self.parent, background="#FFFFFF")
        frame_for_settings.pack()

        # Фрейм для названия турнира
        frame_for_tn_name = tk.Frame(frame_for_settings, background="#FFFFFF")
        frame_for_tn_name.pack(fill="x", pady=5)

        label_tn_name = MyLabels(frame_for_tn_name, text="Название турнира:")
        label_tn_name.pack(side="left", padx=5)

        entry_tn_name = MyEntry(frame_for_tn_name)
        entry_tn_name.pack(side="left", padx=5)

        # Фрейм для пути
        frame_for_path = tk.Frame(frame_for_settings, background="#FFFFFF")
        frame_for_path.pack(fill="x", pady=5)

        label_path = MyLabels(frame_for_path, text="Папка для сохранения турнира:")
        label_path.pack(side="left", padx=5)

        # Переменная, хранящая путь к папке, в которой будет храниться файл
        path = ""

        # Определяем путь к файлу
        def take_path():
            nonlocal path
            directory_path = fd.askdirectory()
            if directory_path != "":
                path = directory_path
                button_select_path.configure(text=path)

        button_select_path = MyButton(frame_for_path, text="Выбрать папку для сохранения", border=1,
                                      command=take_path)
        button_select_path.pack(side="left", padx=5)

        # Фрейм для ФИО судьи
        frame_for_referee_name = tk.Frame(frame_for_settings, background="#FFFFFF")
        frame_for_referee_name.pack(fill="x", pady=5)

        label_referee_name = MyLabels(frame_for_referee_name, text="ФИО судьи:")
        label_referee_name.pack(side="left", padx=5)

        entry_referee_name = MyEntry(frame_for_referee_name)
        entry_referee_name.pack(side="left", padx=5)

        # Фрейм для ФИО помощника судьи
        frame_for_assistant_referee_name = tk.Frame(frame_for_settings, background="#FFFFFF")
        frame_for_assistant_referee_name.pack(fill="x", pady=5)

        label_assistant_referee_name = MyLabels(frame_for_assistant_referee_name, text="ФИО помощника судьи:")
        label_assistant_referee_name.pack(side="left", padx=5)

        entry_assistant_referee_name = MyEntry(frame_for_assistant_referee_name)
        entry_assistant_referee_name.pack(side="left", padx=5)

        # Фрейм для системы проведения турнира
        frame_for_system = tk.Frame(frame_for_settings, background="#FFFFFF")
        frame_for_system.pack(fill="x", pady=5)

        label_system = MyLabels(frame_for_system, text="Система проведения соревнований:")
        label_system.pack(side="left", padx=5)

        systems = ["Швейцарская система", "Олимпийская система", "Круговая система"]
        combobox_system = MyCombobox(frame_for_system, values=systems, state="readonly")
        combobox_system.pack(side="left", padx=5)

        # Фрейм для поля количества туров
        frame_for_count_of_tours = tk.Frame(frame_for_settings, background="#FFFFFF")
        frame_for_count_of_tours.pack(fill="x", pady=5)

        label_count_of_tours = MyLabels(frame_for_count_of_tours, text="Количество туров:")
        label_count_of_tours.pack(side="left", padx=5)

        entry_count_of_tours = MyEntry(frame_for_count_of_tours)
        entry_count_of_tours.pack(side="left", padx=5)

        # Фрейм для поля ввода даты начала соревнований
        frame_for_date_of_start = tk.Frame(frame_for_settings, background="#FFFFFF")
        frame_for_date_of_start.pack(fill="x", pady=5)

        label_date_of_start = MyLabels(frame_for_date_of_start, text="Дата начала турнира:")
        label_date_of_start.pack(side="left", padx=5)

        entry_date_of_start = DateEntry(frame_for_date_of_start, selectmode="day", date_pattern="dd-mm-yyyy",
                                        font=("Times New Roman", 14),
                                        relief="solid",
                                        width=67)
        entry_date_of_start.pack(side="left", padx=5)

        # Фрейм для поля ввода даты окончания соревнований
        frame_for_date_of_end = tk.Frame(frame_for_settings, background="#FFFFFF")
        frame_for_date_of_end.pack(fill="x", pady=5)

        label_date_of_end = MyLabels(frame_for_date_of_end, text="Дата окончания турнира:")
        label_date_of_end.pack(side="left", padx=5)

        entry_date_of_end = DateEntry(frame_for_date_of_end, selectmode="day", date_pattern="dd-mm-yyyy",
                                      font=("Times New Roman", 14),
                                      relief="solid",
                                      width=67)

        # Задаем дату окончания по умолчанию равную дате начала + неделя
        date = entry_date_of_start.get_date() + Calendar.timedelta(days=7)
        entry_date_of_end.set_date(date=date)

        entry_date_of_end.pack(side="left", padx=5)

        # Приоритеты, по которым определяются места
        priorities = ["Система коэффициентов Бухгольца",
                      "Система коэффициентов Шмульяна",
                      "Наибольшее число побед",
                      "Результат личной встречи"]

        # Фрейм для поля ввода приоритета 1
        frame_for_priority_1 = tk.Frame(frame_for_settings, background="#FFFFFF")
        frame_for_priority_1.pack(fill="x", pady=5)

        label_priority_1 = MyLabels(frame_for_priority_1, text="Приоритет 1 при равенстве очков:")
        label_priority_1.pack(side="left", padx=5)

        combobox_priority_1 = MyCombobox(frame_for_priority_1, values=priorities,
                                         state="readonly")
        combobox_priority_1.pack(side="left", padx=5)

        # Фрейм для поля ввода приоритета 2
        frame_for_priority_2 = tk.Frame(frame_for_settings, background="#FFFFFF")
        frame_for_priority_2.pack(fill="x", pady=5)

        label_priority_2 = MyLabels(frame_for_priority_2, text="Приоритет 2 при равенстве очков:")
        label_priority_2.pack(side="left", padx=5)

        combobox_priority_2 = MyCombobox(frame_for_priority_2, values=priorities,
                                         state="readonly")
        combobox_priority_2.pack(side="left", padx=5)

        # Фрейм для поля ввода приоритета 3
        frame_for_priority_3 = tk.Frame(frame_for_settings, background="#FFFFFF")
        frame_for_priority_3.pack(fill="x", pady=5)

        label_priority_3 = MyLabels(frame_for_priority_3, text="Приоритет 3 при равенстве очков:")
        label_priority_3.pack(side="left", padx=5)

        combobox_priority_3 = MyCombobox(frame_for_priority_3, values=priorities,
                                         state="readonly")
        combobox_priority_3.pack(side="left", padx=5)

        # Фрейм для поля ввода приоритета 4
        frame_for_priority_4 = tk.Frame(frame_for_settings, background="#FFFFFF")
        frame_for_priority_4.pack(fill="x", pady=5)

        label_priority_4 = MyLabels(frame_for_priority_4, text="Приоритет 4 при равенстве очков:")
        label_priority_4.pack(side="left", padx=5)

        combobox_priority_4 = MyCombobox(frame_for_priority_4, values=priorities,
                                         state="readonly")
        combobox_priority_4.pack(side="left", padx=5)

        # Фрейм для кнопок далее и назад
        frame_for_buttons = tk.Frame(frame_for_settings, background="#FFFFFF")
        frame_for_buttons.pack(fill="x", pady=5)

        # Проверка корректности ввода данных
        def check_input_data():
            if not (os.path.isdir(path) or os.path.isfile(path)):
                messagebox.showerror(title="Выберите папку",
                                     message="Вы не выбрали папку, в которой будет "
                                             "храниться файл турнира. Сделайте это, "
                                             "прежде чем переходить на следующую страницу.")
                return True
            if not entry_count_of_tours.get().isdigit():
                messagebox.showerror(title="Некорректное количество туров",
                                     message="Вы ввели некорректное количество туров, пожалуйста, введите число.")
                return True
            return False

        # При нажатии кнопки далее вызывается функция next_step
        def next_step():
            if check_input_data():
                return

            data = [entry_tn_name.get(), entry_referee_name.get(), entry_assistant_referee_name.get(),
                    combobox_system.get(), entry_count_of_tours.get(), entry_date_of_start.get_date(),
                    entry_date_of_end.get_date(), combobox_priority_1.get(), combobox_priority_2.get(),
                    combobox_priority_3.get(), combobox_priority_4.get()]


            self.tn.pr1 = combobox_priority_1.get()
            self.tn.pr2 = combobox_priority_2.get()

            # Если объект турнир - пустой, то создаем файл,
            # а также записываем путь к нему в объект турнир
            if self.tn.file_path == "":
                self.tn.file_path = self.create_path_to_file(path, data[0], data[5])
                self.create_excel_file(data)
            # В противном случае просто изменяем необходимые данные, передавая в аргументе также текущий тур
            else:
                # ct - current tour
                ct = tournament.Tournament.get_current_tour(self.tn.file_path)
                self.change_excel_file(data, ct)

            self.create_participants_page()

        button_next_page = MyButton(frame_for_buttons, font=("Times New Roman", 14), text="Далее", width=15,
                                    command=next_step)
        button_next_page.pack(side="right", padx=5)

        button_previous_page = MyButton(frame_for_buttons, font=("Times New Roman", 14), text="Назад", width=15,
                                        command=self.create_start_page)
        button_previous_page.pack(side="left", padx=5)

        # Если мы вернулись со страницы игроков, то заполняем все ячейки
        if self.tn.file_path != "":
            # Достаём все данные из таблицы
            tn_name = tournament.Tournament.get_tn_name(self.tn.file_path)
            referee_name, assistant_referee_name, system, count_of_tours, \
                current_tour, start, end, pr1, pr2, pr3, pr4 = \
                tournament.Tournament.get_all_of_data_without_tn_name(self.tn.file_path)

            # Вставляем данные в соответствующие поля
            entry_tn_name.insert(0, tn_name)

            # Так как в объекте "tournament" хранится путь
            # вместе с названием файла, а при вводе мы выбираем
            # только путь, то необходимо отбросить название
            # файла и после записать путь в кнопку
            index = self.tn.file_path.rindex("/")
            button_select_path.configure(text=self.tn.file_path[: index])

            # Также заполняем переменную path, так как в функции
            # проверки check_input_data мы проверяем содержимое данной переменной
            path = self.tn.file_path[: index]

            # Также во избежание ошибок не даем пользователю поменять путь к файлу,
            # так как файл уже создан
            button_select_path.configure(state="disabled")

            entry_referee_name.insert(0, referee_name)
            entry_assistant_referee_name.insert(0, assistant_referee_name)
            combobox_system.set(system)
            entry_count_of_tours.insert(0, count_of_tours)
            entry_date_of_start.set_date(start)
            entry_date_of_end.set_date(end)

            combobox_priority_1.set(pr1)
            combobox_priority_2.set(pr2)
            combobox_priority_3.set(pr3)
            combobox_priority_4.set(pr4)
