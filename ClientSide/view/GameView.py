import string
import customtkinter as ctk


class GameView(ctk.CTkFrame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.scheduledLabelId = None
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        self.myBoard_frame = ctk.CTkFrame(self)
        self.myBoard_frame.place(relx=0.3, rely=0.5, anchor="center")
        self.create_widgets_for_myBoardframe()

        self.opponentBoard_frame = ctk.CTkFrame(self)
        self.opponentBoard_frame.place(relx=0.7, rely=0.5, anchor="center")
        self.create_widgets_for_opponentBoard_frame()

        self.message_label = ctk.CTkLabel(self, text="", fg_color="Black", font=("Arial", 20))
        self.message_label.place(relx=0.5, rely=0.8, anchor="center")
        self.message_label.place_forget()

    def create_widgets_for_myBoardframe(self):
        self.myBoardButtons = {}  # Dictionary to store button references

        self.myBoardLabel = ctk.CTkLabel(self.myBoard_frame, text="My Board", padx=20, pady=20, font=("Arial", 20))
        self.myBoardLabel.grid(row=0, column=0, padx=20)

        self.grid_frame_myBoard = ctk.CTkFrame(self.myBoard_frame)
        self.grid_frame_myBoard.grid(row=1, column=0, pady=10, padx=20)

        # Create letter labels on the left (vertical axis)
        for i, letter in enumerate(string.ascii_uppercase[:10], start=1):
            ctk.CTkLabel(self.grid_frame_myBoard, text=letter, font=("Arial", 16)).grid(row=i, column=0, padx=5, pady=5)

        # Create number labels on the top (horizontal axis)
        for i in range(10):
            ctk.CTkLabel(self.grid_frame_myBoard, text=str(i), font=("Arial", 16)).grid(row=0, column=i + 1, padx=5, pady=5)

        # Create squares in the grid
        for row in range(10):
            for col in range(10):
                button = ctk.CTkButton(self.grid_frame_myBoard, text="", width=30, height=30)
                button.grid(row=row + 1, column=col + 1, padx=2, pady=2)
                button.configure(state="disabled")  # Disable the button
                self.myBoardButtons[(row, col)] = button

        # Update the grid based on the controller's board
        self.update_myBoard_buttons()

        self.myTable_frame = ctk.CTkFrame(self.myBoard_frame)
        self.myTable_frame.grid(row=2, column=0, pady=10, padx=20)
        self.myBoard_table_labels = []
        self.create_table(self.myTable_frame, self.myBoard_table_labels)

    def update_myBoard_buttons(self):
        for row in range(len(self.controller.client.board.board)):
            for col in range(len(self.controller.client.board.board[row])):
                if self.controller.client.board.board[row][col] >= 1:
                    self.myBoardButtons[(row, col)].configure(fg_color="purple")
                elif self.controller.client.board.board[row][col] == -1:
                    self.myBoardButtons[(row, col)].configure(fg_color="red")

    def create_widgets_for_opponentBoard_frame(self):
        self.opponentBoardButtons = {}

        self.opponentBoardLabel = ctk.CTkLabel(self.opponentBoard_frame, text="Opponent's Board", padx=20, pady=20, font=("Arial", 20))
        self.opponentBoardLabel.grid(row=0, column=0, padx=20)

        self.grid_frame_opponentBoard = ctk.CTkFrame(self.opponentBoard_frame)
        self.grid_frame_opponentBoard.grid(row=1, column=0, pady=10, padx=20)

        # Create letter labels on the left (vertical axis)
        for i, letter in enumerate(string.ascii_uppercase[:10], start=1):
            ctk.CTkLabel(self.grid_frame_opponentBoard, text=letter, font=("Arial", 16)).grid(row=i, column=0, padx=5, pady=5)

        # Create number labels on the top (horizontal axis)
        for i in range(10):
            ctk.CTkLabel(self.grid_frame_opponentBoard, text=str(i), font=("Arial", 16)).grid(row=0, column=i + 1, padx=5, pady=5)

        # Create squares in the grid
        for row in range(10):
            for col in range(10):
                button = ctk.CTkButton(self.grid_frame_opponentBoard, text="", width=30, height=30,
                                       command=lambda r=row, c=col: self.controller.hit(r, c))
                button.grid(row=row + 1, column=col + 1, padx=2, pady=2)
                self.opponentBoardButtons[(row, col)] = button

        self.opponentTable_frame = ctk.CTkFrame(self.opponentBoard_frame)
        self.opponentTable_frame.grid(row=2, column=0, pady=10, padx=20)
        self.opponentBoard_table_labels = []
        self.create_table(self.opponentTable_frame, self.opponentBoard_table_labels)

    def create_table(self, parent, table_labels):
        # Header
        header_frame = ctk.CTkFrame(parent)
        header_frame.grid(row=0, column=0, columnspan=2, pady=(10, 5))

        ctk.CTkLabel(header_frame, text="Ship", font=("Arial", 20)).grid(row=0, column=0, padx=(20, 30), sticky="w")
        ctk.CTkLabel(header_frame, text="Status", font=("Arial", 20)).grid(row=0, column=1, padx=(30, 20), sticky="e")

        # Add a separator
        separator = ctk.CTkFrame(parent, height=2, bg_color="gray")
        separator.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 10))

        # Rows
        for i, ship in enumerate(self.controller.client.board.ships):
            ship_label = ctk.CTkLabel(parent, text=f"{ship}", font=("Arial", 14))
            ship_label.grid(row=i + 2, column=0, padx=(20, 10), sticky="w")

            status_label = ctk.CTkLabel(parent, text="Active", text_color="green", font=("Arial", 14))
            status_label.grid(row=i + 2, column=1, padx=(10, 20), sticky="e")

            table_labels.append((ship_label, status_label))

        # Make sure the grid columns expand evenly
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)

    def show_message(self, message, time):
        if self.scheduledLabelId is not None:
            self.after_cancel(self.scheduledLabelId)
            self.hide_message()
            self.scheduledLabelId = None

        self.message_label.configure(text=message)
        self.message_label.place(relx=0.5, rely=0.8, anchor="center")
        self.scheduledLabelId = self.after(time, self.hide_message)

    def hide_message(self):
        self.message_label.place_forget()

    def disable_button(self, x, y):
        button = self.opponentBoardButtons[(x, y)]
        button.configure(state="disabled")

    def get_status_label_myBoard(self, ship_label):
        for label_pair in self.myBoard_table_labels:
            if label_pair[0].cget("text") == ship_label:
                return label_pair[1]
        return None

    def get_status_label_opponentBoard(self, ship_label):
        for label_pair in self.opponentBoard_table_labels:
            if label_pair[0].cget("text") == ship_label:
                return label_pair[1]
        return None

    def disable_all_buttons(self):
        for button in self.opponentBoardButtons.values():
            button.configure(state="disabled")

