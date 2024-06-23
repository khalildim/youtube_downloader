import os
import pathlib
import platform
import subprocess
from threading import Thread
from tkinter import Menu,messagebox
from tkinter import filedialog

import customtkinter as ctk
from PIL import Image

from audio import YouTubeAudioDownloader
from check_connection import Connection


class Audio(ctk.CTkFrame):
    def __init__(self, master, switch_frame, thumbnail, default_thumb, title):
        super().__init__(master, corner_radius=0, width=514, height=400, fg_color="#2B2933")
        self.thumbnail_label_img = thumbnail
        self.default_thumb = default_thumb
        self.title = title
        self.dw = YouTubeAudioDownloader()
        # Switch buttons
        self.frame_1_btn = ctk.CTkButton(
            self,
            text="Video",
            fg_color="#706E7A",
            command=switch_frame,
            hover_color="#62606B",
            corner_radius=20
        )
        self.frame_1_btn.grid(column=0, row=0, pady=15, padx=10)

        self.switch_to_frame2_btn = ctk.CTkButton(
            self,
            text="Audio",
            fg_color="#62606B",
            hover_color="#62606B",
            corner_radius=20
        )
        self.switch_to_frame2_btn.grid(column=0, row=0, columnspan=2)

        # Load WiFi status images
        self.wifi_on = ctk.CTkImage(
            light_image=Image.open("resources/images/wifi.png"),
            dark_image=Image.open("resources/images/wifi.png"),
            size=(24, 24)
        )
        self.wifi_off = ctk.CTkImage(
            light_image=Image.open("resources/images/no-wifi.png"),
            dark_image=Image.open("resources/images/no-wifi.png"),
            size=(29, 29)
        )

        # WiFi status label
        self.wifi_label = ctk.CTkLabel(
            self,
            text="",
            fg_color="#2B2933",
            bg_color="#2B2933"
        )
        self.wifi_label.grid(row=0, column=1, sticky="e", padx=(0, 120))

        # WiFi status text
        self.wifi_statue_text = ctk.CTkLabel(
            self,
            text="",
            fg_color="#2B2933",
            bg_color="#2B2933",
            font=ctk.CTkFont("ubuntu", 14, weight="bold")
        )
        self.wifi_statue_text.grid(row=0, column=1, columnspan=2, padx=(0, 10), sticky="e")
        self.conn_status(Connection().check())

        # URL entry label
        self.url_text = ctk.CTkLabel(
            self,
            text="U R L :",
            font=ctk.CTkFont("intern", 16, weight="normal", underline=True)
        )
        self.url_text.grid(row=1, column=0, padx=(50, 0), pady=10)

        # URL entry field
        self.url_entry = ctk.CTkEntry(
            self,
            width=296,
            height=41,
            fg_color="#3B3944",
            corner_radius=20,
            border_width=0,
            placeholder_text="Enter Url",

        )
        self.url_entry.grid(row=1, column=1, padx=20, pady=10)
        self.menu = Menu(self, tearoff=False)
        self.menu.add_command(label="Paste", command=lambda: self.paste(self.url_entry))
        # Bind focus events to URL entry field
        self.url_entry.bind("<FocusIn>", self.on_focus_in)
        self.url_entry.bind("<FocusOut>", self.on_focus_out)

        # Bind right-click event to URL entry field
        self.url_entry.bind("<Button-3>", self.show_right_click_menu)

        # Bit rate label
        self.resolution_text = ctk.CTkLabel(
            self,
            text="B i t  R a t e s :",
            font=ctk.CTkFont("intern", 16, weight="normal", underline=True)
        )
        self.resolution_text.grid(row=2, column=0, padx=(50, 0), sticky="w", pady=10)

        # Resolution dropdown menu
        self.resolution = ctk.CTkOptionMenu(
            self,
            values=["320 kbit/s", "256 kbit/s", "192 kbit/s", "128 kbit/s", "96 kbit/s", "32 kbit/s"],
            fg_color="#3B3944",
            width=257,
            height=41,
            corner_radius=20,
            dropdown_fg_color="#3B3944"
        )
        self.resolution.grid(row=2, column=1, pady=10)

        # Directory label
        self.directory_text = ctk.CTkLabel(
            self,
            text="D i r e c t o r y :",
            font=ctk.CTkFont("intern", 16, weight="normal", underline=True)
        )
        self.directory_text.grid(row=3, column=0, padx=(50, 0), pady=10)

        # Directory button
        self.directory_btn = ctk.CTkButton(
            self,
            text="Choose directory",
            font=ctk.CTkFont("intern", 20, weight="normal"),
            width=257,
            height=41,
            fg_color="#3B3944",
            hover_color="#383641",
            corner_radius=20,
            command=self.get_directory
        )
        self.directory_btn.grid(row=3, column=1, pady=10)

        # Save in label
        self.save_in_text = ctk.CTkLabel(
            self,
            text="S a v e  i n :",
            font=ctk.CTkFont("intern", 16, weight="normal", underline=True)
        )
        self.save_in_text.grid(row=4, column=0, padx=(70, 0), sticky="w", pady=10)

        # Chosen directory label
        self.chosen_directory_text = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont("intern", 16, weight="normal", underline=True)
        )
        self.chosen_directory_text.grid(row=4, column=1, pady=10)

        # folder button
        self.folder_img = ctk.CTkImage(
            light_image=Image.open("resources/images/folder.png"),
            dark_image=Image.open("resources/images/folder.png"),
        )
        self.folder_btn = ctk.CTkButton(
            self,
            image=self.folder_img,
            width=32,
            height=32,
            text="",
            corner_radius=20,
            fg_color="#2B2933",
            hover_color="#37353F",
            command=lambda: self.open_folder(self.chosen_directory_text.cget("text"))

        )
        self.folder_btn.grid(row=4, column=1, columnspan=2, pady=10, sticky="se")
        # Download button
        self.download_btn = ctk.CTkButton(
            self,
            text="Download",
            font=ctk.CTkFont("intern", 20, weight="normal"),
            width=128,
            height=41,
            fg_color="#3B3944",
            hover_color="#383641",
            corner_radius=20,
            command=self.download,
        )
        self.download_btn.grid(row=5, column=1, sticky="w", padx=12, pady=10)

        # Search button
        self.search_btn = ctk.CTkButton(
            self,
            text="Search",
            font=ctk.CTkFont("intern", 20, weight="normal"),
            width=128,
            height=41,
            fg_color="#3B3944",
            hover_color="#383641",
            corner_radius=20,
            command=self.search
        )
        self.search_btn.grid(row=5, column=1, sticky="e", padx=12, pady=10)

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(self)
        self.progress_bar.grid(column=1, row=6)
        self.progress_bar.grid_forget()
        self.progress_bar.configure(mode="determinate")

        # Status label
        self.status = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont("intern", 16, weight="normal")
        )
        self.status.grid(row=7, column=1, columnspan=2, rowspan=2, pady=(0, 10), sticky="s")

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
            self.update()
            return True
        else:
            self.wifi_label.configure(image=self.wifi_off)
            self.wifi_label.grid(padx=(0, 120))
            self.wifi_statue_text.configure(text="Disconnected")
            self.update()
            return False

    def download(self):
        if self.conn_status(Connection().check()):
            url = self.url_entry.get()
            bitrate = int(self.resolution.get().split()[0])
            output = self.chosen_directory_text.cget("text")
            if output == "":
                self.status.configure(text="Select downloading folder", text_color="red")
                return None
            self.progress_bar.grid(column=1, row=6)
            def call():
                message = messagebox.askquestion(title="File exist",message="File already exist \nDo you want to overwrite?")
                return message
            def perform_download():
                self.status.configure(text="Downloading...", text_color="green")
                data = self.dw.main(url, bitrate, output,call)
                if data:
                    self.progress_bar.stop()
                    self.progress_bar.configure(mode="determinate")
                    self.progress_bar.set(1)
                    self.status.configure(text="Downloaded", text_color="green")
                    self.after(7000, self.clear_resolution_label)
                elif not data:
                    self.status.configure(text="downloading stopped", text_color="red")
                    self.after(7000, self.clear_resolution_label)
                else:
                    self.status.configure(text=data, text_color="red")
                    self.after(7000, self.clear_resolution_label)
                self.update()

            download_thread = Thread(target=perform_download)
            download_thread.start()

            def update_progress_bar():
                if download_thread.is_alive():
                    self.progress_bar.configure(mode="indeterminate")
                    self.progress_bar.start()
                else:
                    self.progress_bar.set(1)

            update_progress_bar()
        else:
            self.status.configure(text="Please Check connection", text_color="red")
            self.update()
            self.after(7000, self.clear_resolution_label)

    def search(self):
        if self.conn_status(Connection().check()):
            url = self.url_entry.get()
            title, thumbnail = self.dw.search(url)
            self.title.configure(text=title, fg_color="#3C313F")
            self.thumbnail_label_img.configure(image=thumbnail)
        else:
            self.status.configure(text="Please Check connection", text_color="red")
            self.update()
            self.after(7000, self.clear_resolution_label)
    def clear_resolution_label(self):
        self.status.configure(text="")
        self.url_entry.delete(0, ctk.END)
        self.title.configure(text="", fg_color="#3B3944")
        self.resolution.configure(values=[])
        self.thumbnail_label_img.configure(image=self.default_thumb)

    def show_right_click_menu(self, e):
        self.menu.tk_popup(e.x_root, e.y_root)

    def paste(self, widget):
        try:
            clipboard_text = self.clipboard_get()
            widget.insert("insert", clipboard_text)
        except:
            pass

    def open_folder(self, path):
        if path:
            current_path = pathlib.Path(__file__).resolve().parent.parent
            if path == "output/audios":
                path = current_path / path
            # Open the selected folder
            if platform.system() == "Windows":
                os.startfile(path)
            elif platform.system() == "Darwin":  # macOS
                subprocess.Popen(["open", path])
            else:  # Linux and other OS
                subprocess.Popen(["xdg-open", path])
