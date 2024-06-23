import os
import re
import subprocess
import time
from io import BytesIO

import customtkinter as ctk
import requests
from PIL import Image
from pytube import YouTube
import pathlib
from check_connection import Connection


class YouTubeAudioDownloader:
    def __init__(self):
        self.thumbnail_file = "thumbnail.jpg"

    def sanitize_title(self, title):
        """Sanitize the title to remove invalid characters for filenames."""
        return re.sub(r'[<>:"/\\|?*]', '', title).replace(" ", "_")

    def download_thumbnail(self, url, filename, path):
        """Download the thumbnail from the provided URL."""
        response = requests.get(url)
        if response.status_code == 200:
            with open(f"{path}/{filename}", 'wb') as file:
                file.write(response.content)
            print("Thumbnail downloaded successfully.")
        else:
            raise Exception("Failed to download the thumbnail.")

    def get_best_audio_stream(self, result, max_bitrate):
        """Get the best audio stream within the max bitrate limit."""
        audio_streams = result.streams.filter(only_audio=True)
        resolution = [int(stream.abr.replace("kbps", "")) for stream in audio_streams]
        resolution.sort(reverse=True)
        print(f"Available bitrates: {[f'{item}kbps' for item in resolution]}")

        chosen_bitrate = resolution[0]
        for res in resolution:
            if res <= max_bitrate:
                chosen_bitrate = res
                break

        stream = audio_streams.filter(abr=f"{chosen_bitrate}kbps").first()
        return stream, chosen_bitrate

    def download_audio_stream(self, stream, title, path):
        """Download the audio stream."""
        stream.download(filename=title, output_path=path)

    def convert_to_mp3_with_thumbnail(self, title, output_bitrate, path):
        """Convert the downloaded audio to MP3 with the specified bitrate and add the thumbnail."""
        type_st = title.split(".")[-1]
        output_file = title.replace(type_st, "mp3").replace("_", " ")

        ffmpeg_command = [
            'ffmpeg',
            '-i', f"{path}/{title}",
            '-i', f"{path}/{self.thumbnail_file}",
            '-map', '0:a',
            '-map', '1',
            '-c:v', 'mjpeg',
            '-id3v2_version', '3',
            '-b:a', f'{output_bitrate}k',  # Set the audio bitrate
            '-metadata:s:v', 'title=Album cover',
            '-metadata:s:v', 'comment=Cover (front)',
            f"{path}/{output_file}"
        ]

        time.sleep(2)
        subprocess.run(ffmpeg_command, check=True,input=b'y\n')
        print(f"MP3 file created successfully at {output_bitrate}kbps with thumbnail.")
        return output_file

    def cleanup(self, files, path):
        """Remove temporary files."""
        for file in files:
            if os.path.exists(f"{path}/{file}"):
                os.remove(f"{path}/{file}")


    def search(self, url):
        try:
            if Connection():
                result = YouTube(url)
                title = result.title
                thumbnail = result.thumbnail_url
                thumbnail = self.convert_img(thumbnail)
                return title, thumbnail
            else:
                print("connection error")
        except Exception as e:
            print(f"There is an error: {e}")
    def convert_img(self, thumbnail):
        response = requests.get(thumbnail)
        img_data = response.content
        img = Image.open(BytesIO(img_data))
        img.thumbnail((130, 120))
        conv_img = ctk.CTkImage(light_image=img, dark_image=img, size=(125, 110))
        return conv_img

    def main(self, url, max_bitrate, path,call):
        try:
            result = YouTube(url)
            path = pathlib.Path(__file__).parent.parent / path
            stream, chosen_bitrate = self.get_best_audio_stream(result, max_bitrate)
            print(f"Downloading audio at {chosen_bitrate}kbps")

            title = self.sanitize_title(result.title) + "." + stream.mime_type.split("/")[1]
            if self.check_if_exist(file_name=self.sanitize_title(result.title),path=path):
                if call() == "no":
                    return False
            self.download_audio_stream(stream, title, path)

            self.download_thumbnail(result.thumbnail_url, self.thumbnail_file, path)

            output_file = self.convert_to_mp3_with_thumbnail(title, max_bitrate, path)
            return True
        except Exception as e:
            print(f"Error occurred: {e}")
            return f"Error occurred: {e}"
        finally:
            self.cleanup([self.thumbnail_file, title], path)

    @staticmethod
    def check_if_exist(file_name, path):
        # print(path)
        file_name = file_name.replace("_", " ")
        output_path = path / f"{file_name}.mp3"
        
        # print(output_path)
        return output_path.exists()
