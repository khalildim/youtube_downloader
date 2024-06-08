from io import BytesIO
from pathlib import Path
from tkinter import filedialog

import customtkinter as ctk
import requests
from PIL import Image

from check_connection import Connection
from youtube import Downloader

OUTPUT_PATH = Path(__file__).parent


# ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\khali\Desktop\py\Python\video_downloader")


def convert_img(thumbnail):
    response = requests.get(thumbnail)
    img_data = response.content
    img = Image.open(BytesIO(img_data))
    img.thumbnail((130, 120))
    conv_img = ctk.CTkImage(light_image=img, dark_image=img, size=(125, 110))
    return conv_img


class Gui:
    def __init__(self):

        self.app = ctk.CTk()
        self.app.title("video Downloader")
        self.app.geometry("680x400")
        # self.app.resizable(width=False, height=False)
        self.app.configure(fg_color="#2B2933")
        self.app.iconbitmap("resources/images/download.ico")

        # left section
        self.left_frame = ctk.CTkFrame(self.app, width=166, height=400, fg_color="#3B3944")

        self.left_frame.grid(column=0, row=0, rowspan=5, sticky="nsw")

        # video title
        self.video_title = ctk.CTkLabel(self.app, text="V i d e o  T i t l e",
                                        font=ctk.CTkFont("intern", 16, weight="normal", underline=True),
                                        fg_color="#3B3944", bg_color="#3B3944")
        self.video_title.grid(row=0, column=0)

        self.title = ctk.CTkLabel(self.app, text="", font=ctk.CTkFont("intern", 13, weight="normal"),
                                  fg_color="#3B3944", bg_color="#3B3944", wraplength=130, corner_radius=14)
        self.title.grid(row=0, column=0, rowspan=2, pady=(30, 0))

        # thumbnail image
        self.test = ctk.CTkLabel(self.app, text="T h u m b n a i l",
                                 font=ctk.CTkFont("intern", 16, weight="normal", underline=True), fg_color="#3B3944",
                                 bg_color="#3B3944")
        self.test.grid(row=3, column=0)

        self.thumbnail_img = ctk.CTkImage(light_image=Image.open("resources/images/image_2.png"), dark_image=Image.open(
            "resources/images/image_2.png"),
                                          size=(114, 107))
        self.thumbnail_label_img = ctk.CTkLabel(self.app, image=self.thumbnail_img, text="", corner_radius=20,
                                                fg_color="#3B3944", bg_color="#3B3944")
        self.thumbnail_label_img.grid(row=4, column=0)

        # right section
        # wifi test
        self.wifi_on = ctk.CTkImage(light_image=Image.open("resources/images/wifi.png"),
                                    dark_image=Image.open("resources/images/wifi.png"), size=(24, 24))
        self.wifi_off = ctk.CTkImage(light_image=Image.open("resources/images/no-wifi.png"),
                                     dark_image=Image.open("resources/images/no-wifi.png"), size=(29, 29))

        self.wifi_label = ctk.CTkLabel(self.app, text="", fg_color="#2B2933", bg_color="#2B2933")
        self.wifi_label.grid(row=0, column=2, sticky="e", padx=(0, 120))

        # wifi statue text
        self.wifi_statue_text = ctk.CTkLabel(self.app, text="", fg_color="#2B2933", bg_color="#2B2933",
                                             font=ctk.CTkFont("ubuntu", 14, weight="bold"))
        self.wifi_statue_text.grid(row=0, column=2, padx=(0, 10), sticky="e")
        self.conn_status(Connection().check())

        # url entry
        self.url_text = ctk.CTkLabel(self.app, text="U R L :",
                                     font=ctk.CTkFont("intern", 16, weight="normal", underline=True))
        self.url_text.grid(row=1, column=1, padx=(50, 0))

        self.url_entry = ctk.CTkEntry(self.app, width=296, height=41, fg_color="#3B3944", corner_radius=20,
                                      border_width=0, placeholder_text="Enter Url")
        self.url_entry.grid(row=1, column=2, padx=20)
        # url entry event
        self.url_entry.bind("<FocusIn>", self.on_focus_in)
        self.url_entry.bind("<FocusOut>", self.on_focus_out)

        # resolution
        self.resolution_text = ctk.CTkLabel(self.app, text="R e s o l u t i o n :",
                                            font=ctk.CTkFont("intern", 16, weight="normal", underline=True))
        self.resolution_text.grid(row=2, column=1, padx=(50, 0), sticky="w")

        self.resolution = ctk.CTkOptionMenu(self.app, values=[], fg_color="#3B3944", width=257, height=41,
                                            corner_radius=20, dropdown_fg_color="#3B3944")
        self.resolution.grid(row=2, column=2)

        # Directory
        self.directory_text = ctk.CTkLabel(self.app, text="D i r e c t o r y :",
                                           font=ctk.CTkFont("intern", 16, weight="normal", underline=True))
        self.directory_text.grid(row=3, column=1, padx=(50, 0))

        self.directory_btn = ctk.CTkButton(self.app, text="Choose directory",
                                           font=ctk.CTkFont("intern", 20, weight="normal"), width=257, height=41,
                                           fg_color="#3B3944", hover_color="#383641", corner_radius=20,
                                           command=self.get_directory)
        self.directory_btn.grid(row=3, column=2)

        self.save_in_text = ctk.CTkLabel(self.app, text="",
                                         font=ctk.CTkFont("intern", 16, weight="normal", underline=True), )
        self.save_in_text.grid(row=3, rowspan=2, column=1, padx=(70, 0), pady=(5, 25), sticky="w")

        self.chosen_directory_text = ctk.CTkLabel(self.app, text="",
                                                  font=ctk.CTkFont("intern", 16, weight="normal", underline=True))
        self.chosen_directory_text.grid(row=3, rowspan=2, column=2, pady=(5, 25))

        # download and search button

        self.download_btn = ctk.CTkButton(self.app, text="Download", font=ctk.CTkFont("intern", 20, weight="normal"),
                                          width=128, height=41, fg_color="#3B3944", hover_color="#383641",
                                          corner_radius=20, command=self.download)
        self.download_btn.grid(row=4, column=2, sticky="w", padx=12, pady=0)

        self.search_btn = ctk.CTkButton(self.app, text="Search", font=ctk.CTkFont("intern", 20, weight="normal"),
                                        width=128, height=41, fg_color="#3B3944", hover_color="#383641",
                                        corner_radius=20, command=self.start_search)
        self.search_btn.grid(row=4, column=2, sticky="e", padx=12, pady=0)

        # status text
        self.status = ctk.CTkLabel(self.app, text="", font=ctk.CTkFont("intern", 16, weight="normal"))
        self.status.grid(row=4, column=2, columnspan=2, rowspan=2, pady=(0, 10), sticky="s")
        self.app.mainloop()

    def on_focus_in(self, event):
        self.url_entry.configure(border_color="#7D6C6C", border_width=2)

    def on_focus_out(self, event):
        self.url_entry.configure(border_color="#7D6C6C", border_width=0)

    def get_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.chosen_directory_text.configure(text=directory)
            self.save_in_text.configure(text="S a v e  i n :")

    def conn_status(self, status):
        if status:
            self.wifi_label.configure(image=self.wifi_on)
            self.wifi_label.grid(padx=(0, 100))
            self.wifi_statue_text.configure(text="Connected")
            self.app.update()
            return True
        else:
            self.wifi_label.configure(image=self.wifi_off)
            self.wifi_label.grid(padx=(0, 120))
            self.wifi_statue_text.configure(text="Disconnected")
            self.app.update()
            return False

    def start_search(self):
        if self.conn_status(Connection().check()):
            url = self.url_entry.get()
            self.yt = Downloader(url)
            title = self.yt.title
            resolution = self.yt.resolutions
            thumbnail = self.yt.thumbnail
            thumbnail = convert_img(thumbnail)
            self.resolution.configure(values=resolution)
            self.title.configure(text=title, fg_color="#3C313F")
            self.thumbnail_label_img.configure(image=thumbnail)
            print(OUTPUT_PATH)
            self.app.update()
        else:
            self.status.configure(text="Please Check connection", text_color="red")
            self.app.update()
            self.app.after(7000, self.clear_resolution_label)

    def download(self):
        if self.conn_status(Connection().check()):
            path = self.chosen_directory_text.cget("text")
            res = self.resolution.get()
            if path == "":
                data = self.yt.download(res, path=OUTPUT_PATH)
            else:
                data = self.yt.download(res, path)
            if data:
                self.status.configure(text="Downloaded", text_color="green")
            elif not data:
                self.status.configure(text="try to change the resolution", text_color="red")
            else:
                self.status.configure(text=data, text_color="red")
                self.app.update()
            self.app.after(7000, self.clear_resolution_label)
        else:
            self.status.configure(text="please Check connection", text_color="red")
            self.app.update()
            self.app.after(7000, self.clear_resolution_label)

    def clear_resolution_label(self):
        self.status.configure(text="")
        self.url_entry.delete(0, ctk.END)
        self.title.configure(text="", fg_color="#3B3944")
        self.resolution.configure(values=[])
        self.thumbnail_label_img.configure(image=self.thumbnail_img)


if __name__ == "__main__":
    Gui()
