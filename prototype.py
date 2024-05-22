import tkinter as tk
import random


class BattleshipGUI:
    def __init__(self, master):
        self.ships = None
        self.message_label = None
        self.new_game_button = None
        self.buttons = None
        self.board = None
        self.master = master
        self.master.title("Battleship Game")  # Set the title of the window
        self.board_size = 5  # Size of the board
        self.num_ships = 3  # Number of ships
        self.create_widgets()  # Create GUI widgets
        self.new_game()  # Start a new game

    def create_widgets(self):
        # Create buttons for the game grid
        self.buttons = []
        for r in range(self.board_size):
            button_row = []
            for c in range(self.board_size):
                button = tk.Button(self.master, width=2, command=lambda row=r, col=c: self.click(r, c))
                button.grid(row=r, column=c)
                button_row.append(button)
            self.buttons.append(button_row)

        # Button to start a new game
        self.new_game_button = tk.Button(self.master, text="New Game", command=self.new_game)
        self.new_game_button.grid(row=self.board_size, columnspan=self.board_size)

        # Label to display game messages
        self.message_label = tk.Label(self.master, text="")
        self.message_label.grid(row=self.board_size + 1, columnspan=self.board_size)

    def new_game(self):
        # Initialize the board and randomly place ships
        self.board = [[' ' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.ships = []
        for _ in range(self.num_ships):
            ship = (random.randint(0, self.board_size - 1), random.randint(0, self.board_size - 1))
            while ship in self.ships:
                ship = (random.randint(0, self.board_size - 1), random.randint(0, self.board_size - 1))
            self.ships.append(ship)

        # Reset the message label
        self.message_label.config(text="New game started. Guess where the ships are!")

    def click(self, row, col):
        # Handle button clicks
        if (row, col) in self.ships:
            # If the clicked cell contains a ship
            self.board[row][col] = 'X'
            self.buttons[row][col].config(text='X', state='disabled', disabledforeground='red')
            if all(self.board[row][col] == 'X' for row, col in self.ships):
                # Check if all ships are sunk
                self.message_label.config(text="Congratulations! You sunk all the battleships!")
                for row in range(self.board_size):
                    for col in range(self.board_size):
                        self.buttons[row][col].config(state='disabled')
        else:
            # If the clicked cell does not contain a ship
            if self.board[row][col] != ' ':
                return
            self.board[row][col] = 'O'
            self.buttons[row][col].config(text='O', state='disabled', disabledforeground='blue')
            self.message_label.config(text="Miss! Try again.")


def main():
    # Create the Tkinter window and start the game
    root = tk.Tk()
    game = BattleshipGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
