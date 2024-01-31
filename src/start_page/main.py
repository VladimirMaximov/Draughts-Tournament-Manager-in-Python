import tkinter as tk
import new_tournament_creation_page.parameters_frame as parameters_flame


class StartFrame(tk.Frame):

    def __init__(self, parent: tk.Tk):
        tk.Frame.__init__(self, parent, background="#FFFFFF")
        self.parent = parent
        self.set_window()
        self.create_elements()
        self.pack(expand=1)

    def create_parameters_frame(self):
        [child.destroy() for child in self.parent.winfo_children()]
        parameters_flame.ParametersFrame(parent=self.parent)

    def create_elements(self):
        frame_for_label = tk.Frame(self,
                                   background="#FFFFFF",
                                   width=800,
                                   height=100,
                                   border=10
                                   )
        frame_for_label.pack(expand=1)
        frame_for_buttons = tk.Frame(self,
                                     background="#FFFFFF",
                                     width=700,
                                     height=100,
                                     border=10
                                     )
        frame_for_buttons.pack(expand=1)
        label = tk.Label(frame_for_label, text="Шашечный турнирный менеджер",
                         font=("Times New Roman", 40),
                         background="#FFFFFF"
                         )
        label.pack(pady=(20, 0))
        button_new_tournament = tk.Button(frame_for_buttons, text="Новый турнир",
                                          font=("Times New Roman", 14),
                                          background="#FFFFFF",
                                          width=20,
                                          height=2,
                                          relief="solid",
                                          activebackground="#FFFFFF",
                                          command=self.create_parameters_frame
                                          )
        button_new_tournament.pack(side="left", padx=(90, 40), pady=(0, 30))

        button_new_tournament = tk.Button(frame_for_buttons, text="Загрузить турнир",
                                          font=("Times New Roman", 14),
                                          background="#FFFFFF",
                                          width=20,
                                          height=2,
                                          relief="solid",
                                          activebackground="#FFFFFF"
                                          )
        button_new_tournament.pack(side="right", padx=(40, 90), pady=(0, 30))

    def set_window(self):
        width = 1000
        height = 600
        self.parent.title("Турнирный менеджер")
        self.parent.config(bg="#FFFFFF")

        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()

        x = (screen_width - width) / 2
        y = (screen_height - height) / 2

        self.parent.geometry(f"{width}x{height}+{int(x)}+{int(y)}")
        self.parent.resizable(False, False)


def main():
    window = tk.Tk()
    StartFrame(window)
    window.mainloop()


if __name__ == "__main__":
    main()
