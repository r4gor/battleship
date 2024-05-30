import queue
import sys
import time

from EventFactory import EventFactory
from .GameController import GameController
from .SetupController import SetupController
from .LoginController import LoginController
from ..HandleEventFromServer import HandleEventFromServer
import customtkinter as ctk


class Controller:
    def __init__(self, client):
        self.client = client
        self.title = "Battleship"
        self.geometry = "1366x768"
        self.current_controller = None
        self.event_queue = queue.Queue()
        self.mainLoopStarted = False
        self.LoginController = None
        self.SetupController = None
        self.GameController = None

        self.main_window = ctk.CTk()
        self.main_window.geometry(self.geometry)
        self.main_window.title(self.title)
        self.main_window.resizable(False, False)
        self.main_window.protocol("WM_DELETE_WINDOW", self.on_close)

    def start(self):
        self.show_login()
        if not self.mainLoopStarted:
            self.mainLoopStarted = True
            self.main_window.mainloop()

    def processEvents(self):
        while self.event_queue.qsize() > 0:
            event = self.event_queue.get(block=False)
            HandleEventFromServer(self.client, event)
        if self.current_controller:
            self.main_window.after(100, self.processEvents)

    def switch_controller(self, new_controller):
        if self.current_controller is not None:
            self.current_controller.view.pack_forget()
            self.current_controller.view.destroy()
            del self.current_controller
        self.current_controller = new_controller(self)
        self.current_controller.run()

    def addToQueue(self, data):
        self.event_queue.put(data)

    def show_login(self):
        if self.client.getServerHandler() is not None:
            self.client.getServerHandler().stop()
        self.client.reset()
        self.switch_controller(LoginController)

    def show_setup(self):
        self.switch_controller(SetupController)

    def show_game(self):
        self.switch_controller(GameController)

    def on_close(self):
        self.quit()

    def quit(self):
        print('Quitting application...')
        self.main_window.destroy()
        self.main_window.quit()  # Stop the Tkinter main loop
        if self.client.getServerHandler() is not None:
            self.client.getServerHandler().stop()
        self.mainLoopStarted = False
        self.current_controller = None
        del self.main_window
        print('Cleanup done.')
        sys.exit(0)  # Terminate the program

    def restart(self):
        quitEvent = EventFactory("quit")
        self.client.sendEvent(quitEvent)
        self.show_login()
        # self.client.reset()

    def getCurrentController(self):
        return self.current_controller
