import customtkinter as ctk
from PIL import Image

from video_frame import Video
from audio_frame import Audio

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Downloader")
        self.geometry("680x400")
        self.resizable(width=False, height=False)
        self.configure(fg_color="#2B2933")
        self.iconbitmap("resources/images/download.ico")
        # left section
        self.left_frame = ctk.CTkFrame(self, width=166, height=400, fg_color="#3B3944")

        self.left_frame.grid(column=0, row=0, rowspan=5, sticky="nsw")

        # video title
        self.video_title = ctk.CTkLabel(
            self,
            text="V i d e o  T i t l e",
            font=ctk.CTkFont("intern", 16, weight="normal", underline=True),
            fg_color="#3B3944", bg_color="#3B3944"
        )
        self.video_title.grid(row=0, column=0)

        self.title = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont("intern", 13, weight="normal"),
            fg_color="#3B3944",
            bg_color="#3B3944",
            wraplength=130,
            corner_radius=14
        )
        self.title.grid(row=0, column=0, rowspan=3, pady=(26, 0),ipadx=4,ipady=4)

        # thumbnail image
        self.test = ctk.CTkLabel(
            self,
            text="T h u m b n a i l",
            font=ctk.CTkFont("intern", 16, weight="normal", underline=True),
            fg_color="#3B3944",
            bg_color="#3B3944",
        )
        self.test.grid(row=3, column=0)

        self.thumbnail_img = ctk.CTkImage(
            light_image=Image.open("resources/images/image_22.png"),
            dark_image=Image.open("resources/images/image_22.png"),
            size=(114, 107),
        )
        self.thumbnail_label_img = ctk.CTkLabel(
            self,
            image=self.thumbnail_img,
            text="",
            corner_radius=20,
            fg_color="#3B3944", bg_color="#3B3944"
        )
        self.thumbnail_label_img.grid(row=4, column=0)

        # Initialize frames
        self.video_frame = Video(
            self,
            self.show_frame2,
            self.thumbnail_label_img,
            self.thumbnail_img,
            self.title
        )
        self.audio_frame = Audio(
            self,
            self.show_frame1,
            self.thumbnail_label_img,
            self.thumbnail_img,
            self.title
        )

        # Pack the first frame initially
        self.video_frame.grid(column=1, row=0, rowspan=5, sticky="ne")

    def show_frame1(self):
        self.audio_frame.grid_forget()
        self.video_frame.grid(column=1, row=0, rowspan=5, sticky="ne")

    def show_frame2(self):
        self.video_frame.grid_forget()
        self.audio_frame.grid(column=1, row=0, rowspan=5, sticky="ne")

if __name__ == "__main__":
    app = App()
    app.mainloop()
