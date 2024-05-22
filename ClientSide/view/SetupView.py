import customtkinter as ctk
import string


class SetupView(ctk.CTk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.geometry(controller.mainController.geometry)
        self.title(controller.mainController.title)
        self.resizable(False, False)
        self.create_widgets()

    def create_widgets(self):
        # Create a main frame to center the grid
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Create the grid
        self.grid_frame = ctk.CTkFrame(self.main_frame)
        self.grid_frame.grid(row=0, column=0, pady=20, padx=20)

        # Create letter labels on the left (vertical axis)
        for i, letter in enumerate(string.ascii_uppercase[:10], start=1):
            label = ctk.CTkLabel(self.grid_frame, text=letter, font=("Arial", 16))
            label.grid(row=i, column=0, padx=5, pady=5)

        # Create number labels on the top (horizontal axis)
        for i in range(1, 11):
            label = ctk.CTkLabel(self.grid_frame, text=str(i), font=("Arial", 16))
            label.grid(row=0, column=i, padx=5, pady=5)

        # Create clickable squares in the grid
        for row in range(1, 11):
            for col in range(1, 11):
                button = ctk.CTkButton(self.grid_frame, text="", width=30, height=30,
                                       command=lambda r=row, c=col: self.on_square_click(r, c))
                button.grid(row=row, column=col, padx=2, pady=2)

        # Create labels and inputs for coordinates at the bottom
        self.coord_frame = ctk.CTkFrame(self.main_frame)
        self.coord_frame.grid(row=1, column=0, pady=20)

        self.coord_labels = []
        ships = ["Carrier (5 spaces)",
                 "Battleship (4 spaces)",
                 "Cruiser (3 spaces)",
                 "Submarine (3 spaces)",
                 "Destroyer (2 spaces)"]
        for i in range(5):
            label = ctk.CTkLabel(self.coord_frame, text=f"{ships[i]}", font=("Arial", 16))
            label.grid(row=i, column=0, padx=5, pady=5)
            self.coord_labels.append(label)

            input1 = ctk.CTkEntry(self.coord_frame, width=50, font=("Arial", 16))
            input1.grid(row=i, column=1, padx=5, pady=5)

            input2 = ctk.CTkEntry(self.coord_frame, width=50, font=("Arial", 16))
            input2.grid(row=i, column=2, padx=5, pady=5)

    def on_square_click(self, row, col):
        print(f"Square clicked: Row {row}, Column {col}")
