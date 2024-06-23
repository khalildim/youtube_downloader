import pathlib
import subprocess
from pprint import pprint

from pytube import YouTube
import os
from check_connection import Connection
import re

class Downloader:
    def __init__(self, url):
        try:
            if Connection():
                self.url = url
                self.yt = YouTube(url)
                self.title = self.yt.title
                self.thumbnail = self.yt.thumbnail_url

                # Extract available resolutions
                self.resolutions = [stream.resolution for stream in self.yt.streams if stream.resolution]
                # pprint(self.yt.streams)

                # Remove duplicates and sort resolutions in descending order
                self.resolutions = sorted(set(int(res[:-1]) for res in self.resolutions), reverse=True)

                # Convert resolutions back to the original format
                self.resolutions = [f"{res}p" for res in self.resolutions]

            else:
                self.conn = False

        except Exception as e:
            print(f"There is an error: {e}")

    def sanitize_title(self, title):
        """Sanitize the title to remove invalid characters for filenames."""
        return re.sub(r'[<>:"/\\|?*]', '', title).replace(" ", "_")

    def download(self, res, output_path,call):
        try:

            output_path = pathlib.Path(__file__).parent.parent/output_path

            # Get the highest resolution video stream
            video_stream = self.yt.streams.filter(progressive=False, resolution=res).first()
            if self.check_if_exist(file_name=video_stream.title,path=output_path):
                if call() == "no":
                    return False
            video_path = video_stream.download(output_path=output_path, filename='video') if video_stream else None
            audio_stream = self.yt.streams.filter(only_audio=True).order_by('abr').desc().first()
            audio_path = audio_stream.download(output_path=output_path, filename='audio') if audio_stream else None

            if video_path and audio_path:
                merged_video_path = output_path / f"{self.sanitize_title(video_stream.title)}.mp4"
                self.merge_video_audio(video_path, audio_path, merged_video_path)
                return video_path, audio_path
            else:
                return None, None
        except Exception as e:
            print(f"Error downloading video or audio: {e}")
            return None, None
    @staticmethod
    def merge_video_audio(video_path, audio_path, output_path):
        try:
            cmd = ['ffmpeg', '-i', video_path, '-i', audio_path, '-c:v', 'copy', '-c:a', 'aac', '-strict',
                   'experimental', output_path]
            subprocess.run(cmd, check=True,input=b'y\n')
            print(f"Merged video and audio saved at: {output_path}")
            os.remove(video_path)
            os.remove(audio_path)
        except subprocess.CalledProcessError as e:
            print(f"Error merging video and audio: {e}")


    def check_if_exist(self,file_name, path):
        output_path = path / f"{self.sanitize_title(file_name)}.mp4"
        return output_path.exists()


