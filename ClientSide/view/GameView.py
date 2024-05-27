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

    def update_myBoard_buttons(self):
        for row in range(len(self.controller.client.board.board)):
            for col in range(len(self.controller.client.board.board[row])):
                if self.controller.client.board.board[row][col] >= 1:
                    self.myBoardButtons[(row, col)].configure(fg_color="purple")

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
                button = ctk.CTkButton(self.grid_frame_opponentBoard, text="", width=30, height=30)
                button.grid(row=row + 1, column=col + 1, padx=2, pady=2)
                self.opponentBoardButtons[(row, col)] = button
