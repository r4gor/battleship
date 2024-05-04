
class Ship:
    def __init__(self):
        self.length = 0
        self.orientation = "vertical"

    def rotate(self):
        if self.orientation == "vertical":
            self.orientation = "horizontal"
        else:
            self.orientation = "vertical"

