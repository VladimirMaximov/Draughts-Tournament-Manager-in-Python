import tkinter as tk
import new_tournament_creation_page as nt_page
import tournament_and_results_table


class ParticipantsFrame(tk.Frame):
    players = []

    def __init__(self, parent: tk.Tk, tn: tournament_and_results_table.Tournament, players=None):
        tk.Frame.__init__(self, parent, background="#FFFFFF")
        if players is None:
            self.players = []
        else:
            self.players = players
        self.parent = parent
        self.tn = tn
        self.create_elements()
        self.pack(expand=1)

    def create_parameters_frame(self):
        [child.destroy() for child in self.parent.winfo_children()]
        nt_page.ParametersFrame(parent=self.parent, tn=self.tn, players=self.players)

    def create_elements(self):
        # fft - frame for text
        fft = tk.Frame(self,
                       background="#FFFFFF",
                       width=1000,
                       height=60
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

        label0 = tk.Label(fft, text="Добавление участников",
                          font=("Times New Roman", 36),
                          background="#FFFFFF",
                          width=36)
        label0.grid(row=0, column=0, pady=5, padx=10, columnspan=2)

        label1 = tk.Label(fft,
                          text="Введите ФИО участника: ",
                          font=("Times New Roman", 14),
                          background="#FFFFFF",
                          width=23,
                          anchor="w"
                          )
        label1.grid(row=1, column=0, sticky="w", pady=5, padx=(7, 5))

        def add_player(event=None):
            if entry1.get() != "":
                new_player = entry1.get()
                self.players.append(new_player)
                players_var.set([f" {i + 1}. " + self.players[i] for i in range(len(self.players))])
                entry1.delete(0, tk.END)

        def delete_player():
            selection = listbox.curselection()
            if len(selection) != 0:
                self.players.pop(selection[0])
                players_var.set([f" {i + 1}. " + self.players[i] for i in range(len(self.players))])
                listbox.selection_clear(0, tk.END)
            else:
                player_to_remove = entry1.get()
                if self.players.count(player_to_remove) != 0:
                    self.players.remove(player_to_remove)
                    players_var.set([f" {i + 1}. " + self.players[i] for i in range(len(self.players))])
                    entry1.delete(0, tk.END)

        def set_entry1(event):
            selection = listbox.curselection()
            if len(selection) != 0:
                set_player = listbox.get(selection[0])
                entry1.delete(0, tk.END)
                entry1.insert(0, " ".join(set_player.split()[1:]))

        player = tk.StringVar()
        entry1 = tk.Entry(fft,
                          font=("Times New Roman", 14),
                          background="#E8E8E8",
                          relief="flat",
                          width=81,
                          textvariable=player
                          )
        entry1.grid(row=1, column=1, sticky="w", pady=5, padx=(5, 5))
        entry1.bind("<Return>", add_player)

        players_var = tk.Variable(value=[f" {i + 1}. " + self.players[i] for i in range(len(self.players))])
        listbox = tk.Listbox(ffp,
                             relief="solid",
                             border=2,
                             font=("Times New Roman", 14),
                             selectbackground="#E8E8E8",
                             listvariable=players_var,
                             width=106,
                             height=18)
        listbox.pack(anchor="sw", side="left", fill="both", padx=5, pady=5)
        listbox.bind("<<ListboxSelect>>", set_entry1)

        scrollbar = tk.Scrollbar(ffp, orient="vertical", command=listbox.yview)
        scrollbar.pack(anchor="sw", side="right", fill="y", padx=(5, 11), pady=5)
        listbox["yscrollcommand"] = scrollbar.set

        button_back = tk.Button(ffb, text="Назад",
                                font=("Times New Roman", 14),
                                background="#FFFFFF",
                                width=20,
                                height=2,
                                relief="solid",
                                activebackground="#FFFFFF",
                                command=self.create_parameters_frame
                                )
        button_back.grid(row=0, column=0, sticky="W", padx=(5, 25), pady=5)

        button_delete = tk.Button(ffb,
                                  text="Удалить",
                                  font=("Times New Roman", 14),
                                  background="#FFFFFF",
                                  width=20,
                                  height=2,
                                  relief="solid",
                                  activebackground="#FFFFFF",
                                  command=delete_player
                                  )
        button_delete.grid(row=0, column=1, sticky="W", padx=25, pady=5)

        button_add = tk.Button(ffb,
                               text="Добавить",
                               font=("Times New Roman", 14),
                               background="#FFFFFF",
                               width=20,
                               height=2,
                               relief="solid",
                               activebackground="#FFFFFF",
                               command=add_player
                               )
        button_add.grid(row=0, column=2, sticky="W", padx=25, pady=5)

        button_next = tk.Button(ffb, text="Далее",
                                font=("Times New Roman", 14),
                                background="#FFFFFF",
                                width=20,
                                height=2,
                                relief="solid",
                                activebackground="#FFFFFF"
                                )
        button_next.grid(row=0, column=3, sticky="W", padx=(20, 5), pady=5)
