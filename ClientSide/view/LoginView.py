import customtkinter as ctk
from PIL import Image
import os


class LoginView(ctk.CTkFrame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.scheduledLabelId = None
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        script_dir = os.path.dirname(__file__)
        self.logo = ctk.CTkImage(
            dark_image=Image.open(script_dir + "../../../assets/logo.png"),
            light_image=Image.open(script_dir + "../../../assets/logo.png"),
            size=Image.open(script_dir + "../../../assets/logo.png").size
        )

        self.logo_label = ctk.CTkLabel(self, image=self.logo, text='')
        self.logo_label.pack(pady=20)

        self.label = ctk.CTkLabel(self, text="Login", font=("Arial", 60))
        self.label.pack()

        self.frame = ctk.CTkFrame(self, corner_radius=20)
        self.frame.place(relx=0.5, rely=0.65, anchor="center")

        self.label_username = ctk.CTkLabel(self.frame, text="Enter your username:", font=("Arial", 20))
        self.label_username.pack(pady=10, padx=50)
        self.username_entry = ctk.CTkEntry(self.frame, width=200, font=("Arial", 20))
        self.username_entry.pack()

        self.label_lobby = ctk.CTkLabel(self.frame, text="Enter lobby ID:", font=("Arial", 20))
        self.label_lobby.pack(pady=10, padx=50)
        self.lobby_entry = ctk.CTkEntry(self.frame, width=200, font=("Arial", 20))
        self.lobby_entry.pack()
        self.lobby_entry.insert(0, "123")


        self.label_ip = ctk.CTkLabel(self.frame, text="Server IP:", font=("Arial", 20))
        self.label_ip.pack(pady=10)
        self.ip_entry = ctk.CTkEntry(self.frame, width=200, font=("Arial", 20))
        self.ip_entry.pack()
        self.ip_entry.insert(0, "localhost")

        self.label_port = ctk.CTkLabel(self.frame, text="Server Port:", font=("Arial", 20))
        self.label_port.pack(pady=10)
        self.port_entry = ctk.CTkEntry(self.frame, width=200, font=("Arial", 20))
        self.port_entry.pack()
        self.port_entry.insert(0, "5555")

        self.login_button = ctk.CTkButton(self.frame, text="Login", command=self.controller.connect, font=("Arial", 20))
        self.login_button.pack(pady=20)

        self.message_label = ctk.CTkLabel(self.frame, text="", fg_color="Black", font=("Arial", 20))
        self.message_label.pack()
        self.message_label.pack_forget()

    def show_message(self, message):
        if self.scheduledLabelId is not None:
            self.after_cancel(self.scheduledLabelId)
            self.hide_message()
            self.scheduledLabelId = None

        self.message_label.configure(text=message)
        self.message_label.pack()
        self.scheduledLabelId = self.after(5000, self.hide_message)

    def hide_message(self):
        self.message_label.pack_forget()
