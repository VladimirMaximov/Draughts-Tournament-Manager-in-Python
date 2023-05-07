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

    def create_elements(self):
        # fft - frame for text
        fft = tk.Frame(self,
                       background="#FFFF11",
                       width=1000,
                       height=100
                       )
        fft.pack(expand=1, fill="both")
        # ffp - frame for participants
        ffp = tk.Frame(self,
                       background="#FF11FF",
                       width=1000,
                       height=400
                       )
        ffp.pack(expand=1, fill="both")
        # ffb - frame for buttons
        ffb = tk.Frame(self,
                       background="#111FFF",
                       width=1000,
                       height=100
                       )
        ffb.pack(expand=1, fill="both")

        label0 = tk.Label(fft, text=f"Тур №{self.tn.current_tour}",
                          font=("Times New Roman", 36),
                          background="#FFFFFF",
                          width=36)
        label0.pack(expand=1, fill="both")

        canvas = tk.Canvas(ffp, width=950, height=400, bg="#000000")
        canvas.pack(expand=1, side="left")

        scrollbar = tk.Scrollbar(ffp, orient="vertical", command=canvas.yview)
        scrollbar.pack(anchor="sw", side="right", fill="y", padx=(5, 11), pady=5)
        canvas["yscrollcommand"] = scrollbar.set

        button_back = tk.Button(ffb, text="Назад",
                                font=("Times New Roman", 14),
                                background="#FFFFFF",
                                width=20,
                                height=2,
                                relief="solid",
                                activebackground="#FFFFFF",
                                command=self.create_prev_frame
                                )
        button_back.grid(row=0, column=0, sticky="W", padx=(5, 25), pady=5)

        button_delete = tk.Button(ffb,
                                  text="Удалить",
                                  font=("Times New Roman", 14),
                                  background="#FFFFFF",
                                  width=20,
                                  height=2,
                                  relief="solid",
                                  activebackground="#FFFFFF"
                                  )
        button_delete.grid(row=0, column=1, sticky="W", padx=25, pady=5)

        button_add = tk.Button(ffb,
                               text="Просмотр таблицы",
                               font=("Times New Roman", 14),
                               background="#FFFFFF",
                               width=20,
                               height=2,
                               relief="solid",
                               activebackground="#FFFFFF"
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
