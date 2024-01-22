import tkinter as tk
import new_tournament_creation_page as nt_page
import tournament_and_results_table as tart
import tour_draw_page as td_page
from tkinter import messagebox


class ParticipantsFrame(tk.Frame):

    def __init__(self, parent: tk.Tk, tn: tart.Tournament):
        tk.Frame.__init__(self, parent, background="#FFFFFF")
        self.parent = parent
        self.tn = tn
        self.create_elements()
        self.pack(expand=1)

    def create_parameters_frame(self):
        [child.destroy() for child in self.parent.winfo_children()]
        nt_page.ParametersFrame(parent=self.parent, tn=self.tn)

    def create_tours_frame(self):
        pass

    def create_elements(self):
        frame_for_label = tk.Frame(self,
                                   background="#FFFFFF",
                                   width=1000,
                                   height=50
                                   )

        frame_for_label.pack(expand=1, fill="both")
        frame_for_entry = tk.Frame(self,
                                   background="#FFFFFF",
                                   width=1000,
                                   height=50
                                   )

        frame_for_entry.pack(expand=1, fill="both")
        frame_for_listbox = tk.Frame(self,
                                  background="#FFFFFF",
                                  width=1000,
                                  height=400
                                  )

        frame_for_listbox.pack(expand=1, fill="both")
        frame_for_buttons = tk.Frame(self,
                                     background="#FFFFFF",
                                     width=1000,
                                     height=100
                                     )
        frame_for_buttons.pack(expand=1, fill="both")

        label0 = tk.Label(frame_for_label, text="Добавление участников",
                          font=("Times New Roman", 36),
                          background="#FFFFFF",
                          width=36)
        label0.pack()

        label1 = tk.Label(frame_for_entry,
                          text="Введите ФИО участника: ",
                          font=("Times New Roman", 14),
                          background="#FFFFFF",
                          width=23,
                          anchor="w"
                          )
        label1.pack(side="left")

        def add_player(event=None):

            # Если поле не пустое, тогда добавляем нового игрока
            if entry1.get() != "":
                # Достаем имя игрока
                new_player = entry1.get()

                # Добавляем игрока в список игроков
                self.tn.players.append(tart.Player(len(self.tn.players) + 1, new_player))

                # Обновляем список игроков в виджете Text
                players_var.set([f" {i + 1}. " + self.tn.players[i].name for i in range(len(self.tn.players))])

                # Очищаем поле ввода имени
                entry1.delete(0, tk.END)

        def delete_player():

            # Получаем кортеж индексов выделенных строк
            selection = listbox.curselection()

            # Если выделена хотя бы одна строка
            if len(selection) != 0:
                # Удаляем первую строку, которая была выделена
                self.tn.players.pop(selection[0])

                # Обновляем список игроков в виджете Text
                players_var.set([f" {i + 1}. " + self.tn.players[i].name for i in range(len(self.tn.players))])

                # Снимаем выделение с полей
                listbox.selection_clear(0, tk.END)

        def edit_player():

            # Получаем кортеж индексов выделенных строк
            selection = listbox.curselection()

            # Если выделена хотя бы одна строка
            if len(selection) != 0:

                # Изменяем первую строку, которая была выделена
                self.tn.players[selection[0]] = tart.Player(selection[0], entry1.get())

                # Обновляем список игроков в виджете Text
                players_var.set([f" {i + 1}. " + self.tn.players[i].name for i in range(len(self.tn.players))])

                # Снимаем выделение с полей
                listbox.selection_clear(0, tk.END)

        # Функция, которая задает в поле ввода имя то значение, которое выделено
        def set_entry1(event):
            selection = listbox.curselection()
            if len(selection) != 0:
                set_player = listbox.get(selection[0])
                entry1.delete(0, tk.END)
                entry1.insert(0, " ".join(set_player.split()[1:]))

        # Переменная поля entry1
        player = tk.StringVar()
        entry1 = tk.Entry(frame_for_entry,
                          font=("Times New Roman", 14),
                          background="#E8E8E8",
                          relief="flat",
                          width=81,
                          textvariable=player
                          )
        entry1.pack(side="left")
        entry1.bind("<Return>", add_player)

        players_var = tk.Variable(value=[f" {i + 1}. " + self.tn.players[i].name for i in range(len(self.tn.players))])
        listbox = tk.Listbox(frame_for_listbox,
                             relief="solid",
                             border=2,
                             font=("Times New Roman", 14),
                             selectbackground="#E8E8E8",
                             listvariable=players_var,
                             width=106,
                             height=16)
        listbox.pack(anchor="sw", side="left", fill="both", padx=5, pady=5)
        listbox.bind("<<ListboxSelect>>", set_entry1)

        scrollbar = tk.Scrollbar(frame_for_listbox, orient="vertical", command=listbox.yview)
        scrollbar.pack(anchor="sw", side="right", fill="y", padx=(5, 11), pady=5)
        listbox["yscrollcommand"] = scrollbar.set

        button_back = tk.Button(frame_for_buttons, text="Назад",
                                font=("Times New Roman", 14),
                                background="#FFFFFF",
                                width=18,
                                height=2,
                                relief="solid",
                                activebackground="#FFFFFF",
                                command=self.create_parameters_frame
                                )
        button_back.pack(side="left", padx=5, pady=10)

        button_delete = tk.Button(frame_for_buttons,
                                  text="Удалить",
                                  font=("Times New Roman", 14),
                                  background="#FFFFFF",
                                  width=18,
                                  height=2,
                                  relief="solid",
                                  activebackground="#FFFFFF",
                                  command=delete_player
                                  )
        button_delete.pack(side="left", padx=5, pady=10)

        button_add = tk.Button(frame_for_buttons,
                               text="Редактировать",
                               font=("Times New Roman", 14),
                               background="#FFFFFF",
                               width=18,
                               height=2,
                               relief="solid",
                               activebackground="#FFFFFF",
                               command=edit_player
                               )
        button_add.pack(side="left", padx=5, pady=10)

        button_add = tk.Button(frame_for_buttons,
                               text="Добавить",
                               font=("Times New Roman", 14),
                               background="#FFFFFF",
                               width=18,
                               height=2,
                               relief="solid",
                               activebackground="#FFFFFF",
                               command=add_player
                               )
        button_add.pack(side="left", padx=5, pady=10)

        button_next = tk.Button(frame_for_buttons, text="Далее",
                                font=("Times New Roman", 14),
                                background="#FFFFFF",
                                width=18,
                                height=2,
                                relief="solid",
                                activebackground="#FFFFFF",
                                command=self.create_tours_frame
                                )
        button_next.pack(side="left", padx=5, pady=10)
