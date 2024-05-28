import customtkinter as ctk
import string
import textwrap


class SetupView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.scheduledLabelId = None
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        # Create a main frame to center the grid
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.create_widgets_for_mainframe()

        self.left_frame = ctk.CTkFrame(self)
        self.left_frame.place(relx=0.05, rely=0.5, anchor="w")
        self.create_widgets_for_leftframe()

        self.right_frame = ctk.CTkFrame(self)
        self.right_frame.place(relx=0.75, rely=0.9, anchor="w")
        self.create_widgets_for_rightframe()

    def show_finish_setup_message(self):
        self.finish_setup_message.grid(row=0, column=0, padx=10, pady=10)

    def create_widgets_for_rightframe(self):
        self.finish_setup_message = ctk.CTkLabel(self.right_frame,
                                                 text="Waiting for your opponent ...",
                                                 font=("Arial", 20),
                                                 text_color="turquoise")

        self.readyButton = ctk.CTkButton(self.right_frame, text="Ready", font=("Arial", 20), fg_color="green")
        self.readyButton.configure(
            command=lambda: self.controller.ready()
        )
        self.readyButton.grid(row=1, column=0, padx=20, pady=20)


    def create_widgets_for_leftframe(self):
        self.lobbylabel = ctk.CTkLabel(self.left_frame, text=f"Lobby: {self.controller.client.lobbyID}", font=("Arial", 45))
        self.lobbylabel.grid(row=0, column=0, pady=80, padx=5)

        description_text = "Place your ships on the board by specifying the [start] and [end] coordinate. Ex: A4 A8"
        wrapped_text = textwrap.wrap(description_text, width=40)
        self.description = ctk.CTkLabel(self.left_frame,
                                        text="\n".join(wrapped_text),
                                        font=("Arial", 20)
                                        )
        self.description.grid(row=1, column=0, pady=5, padx=5)

    def create_widgets_for_mainframe(self):
        # Create the grid
        self.grid_frame = ctk.CTkFrame(self.main_frame)
        self.grid_frame.grid(row=0, column=0, pady=20, padx=20)

        # Create letter labels on the left (vertical axis)
        for i, letter in enumerate(string.ascii_uppercase[:10], start=1):
            label = ctk.CTkLabel(self.grid_frame, text=letter, font=("Arial", 16))
            label.grid(row=i, column=0, padx=5, pady=5)

        # Create number labels on the top (horizontal axis)
        for i in range(0, 10):
            label = ctk.CTkLabel(self.grid_frame, text=str(i), font=("Arial", 16))
            label.grid(row=0, column=i + 1, padx=5, pady=5)

        self.buttons = {}  # Dictionary to store button references
        # Create squares in the grid
        for row in range(0, 10):
            for col in range(0, 10):
                button = ctk.CTkButton(self.grid_frame, text="", width=30, height=30)
                button.grid(row=row + 1, column=col + 1, padx=2, pady=2)
                button.configure(state="disabled")  # Disable the button
                self.buttons[(row, col)] = button

        # Create labels and inputs for coordinates at the bottom
        self.coord_frame = ctk.CTkFrame(self.main_frame)
        self.coord_frame.grid(row=1, column=0, pady=20, padx=5)

        for i, ship in enumerate(self.controller.client.board.ships):
            label = ctk.CTkLabel(self.coord_frame,
                                 text=f"{ship} ({self.controller.client.board.ships[ship]["requiredSpaces"]} required spaces)",
                                 font=("Arial", 16))
            label.grid(row=i, column=0, padx=5, pady=5)

            input1 = ctk.CTkEntry(self.coord_frame, width=50, font=("Arial", 16))
            input1.grid(row=i, column=1, padx=5, pady=5)

            input2 = ctk.CTkEntry(self.coord_frame, width=50, font=("Arial", 16))
            input2.grid(row=i, column=2, padx=5, pady=5)

            button = ctk.CTkButton(self.coord_frame, text="Place Ship", font=("Arial", 12))
            button.configure(
                command=lambda s=ship.split(" ")[0], btn=button, i1=input1, i2=input2:
                self.controller.placeShip(s, btn, i1, i2)
            )
            button.grid(row=i, column=3, padx=5, pady=5)

            #TODO: delete autocomplete
            letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
            input1.insert(0, letters[i] + '1')
            input2.insert(0, letters[i] + f'{self.controller.client.board.ships[ship]["requiredSpaces"]}')


        self.message_label = ctk.CTkLabel(self.main_frame, text="", fg_color="Black", font=("Arial", 20))
        self.message_label.grid(row=2, column=0, padx=5, pady=5)
        self.message_label.grid_remove()

    def change_button_color(self, row, col, color):
        button = self.buttons.get((row, col))
        if button:
            button.configure(fg_color=color)

    def show_message(self, message):
        if self.scheduledLabelId is not None:
            self.after_cancel(self.scheduledLabelId)
            self.hide_message()
            self.scheduledLabelId = None

        self.message_label.configure(text=message)
        self.message_label.grid(row=2, column=0, padx=5, pady=5)
        self.scheduledLabelId = self.after(5000, self.hide_message)

    def hide_message(self):
        self.message_label.grid_remove()
