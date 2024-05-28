from ClientSide.view.SetupView import SetupView
from EventFactory import EventFactory


class SetupController:
    def __init__(self, controller):
        self.mainController = controller
        self.client = controller.client
        self.view = SetupView(controller.main_window, self)
        self.fullSetup = {}

    def run(self):
        self.view.pack(fill="both", expand=True)

    def showResponse(self, response):
        self.view.show_message(response)

    def placeShip(self, ship, button, input1, input2):
        coord1 = input1.get().upper()
        coord2 = input2.get().upper()
        if coord1 == '' or coord2 == '':
            self.showResponse("Please insert both coordinates")
        elif (len(coord1) != 2 or len(coord2) != 2
                or ord(coord1[0]) < ord('A') or ord(coord1[0]) > ord('J')
                or ord(coord2[0]) < ord('A') or ord(coord2[0]) > ord('J')
                or ord(coord1[1]) < ord('0') or ord(coord1[1]) > ord('9')
                or ord(coord2[1]) < ord('0') or ord(coord2[1]) > ord('9')):
            self.showResponse("Coordinates are not valid")
        else:
            if self.client.board.placeShip(ship, coord1+':'+coord2):
                self.showResponse("Successfully placed ship")
                self.move_and_color(coord1, coord2, 'purple')
                self.fullSetup[ship] = coord1+':'+coord2
                input1.configure(state='disabled')
                input2.configure(state='disabled')
                button.configure(state='disabled')
            else:
                self.showResponse("Can't place ship there!\nPlease check coordinates again")

    @staticmethod
    def convert_coord(coord):
        letter = coord[0].upper()
        number = int(coord[1:])
        col = number
        row = ord(letter) - ord('A')
        return row, col

    def move_and_color(self, start, end, color):
        start_row, start_col = self.convert_coord(start)
        end_row, end_col = self.convert_coord(end)

        row_step = 1 if start_row < end_row else -1
        col_step = 1 if start_col < end_col else -1

        for row in range(start_row, end_row + row_step, row_step):
            for col in range(start_col, end_col + col_step, col_step):
                self.view.change_button_color(row, col, color)

    def ready(self):
        if len(self.fullSetup) == 5:
            event = EventFactory("setup", **self.fullSetup)
            self.client.sendEvent(event)
            self.view.show_finish_setup_message()
            self.view.readyButton.configure(state='disabled')
        else:
            self.showResponse("Place all the ships first!")
