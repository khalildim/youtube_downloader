

from pytube import YouTube
from check_connection import Connection

class Downloader:
    def __init__(self,url):
        # search section
        self.yd = None
        try:
            # check connection
            if Connection():
                self.url = url
                self.yt = YouTube(url)
                self.title = self.yt.title
                self.thumbnail = self.yt.thumbnail_url
                # Extract available resolutions
                self.resolutions = [stream.resolution for stream in self.yt.streams if stream.resolution]

                # Remove duplicates and sort resolutions in descending order
                self.resolutions = sorted(set(int(res[:-1]) for res in self.resolutions), reverse=True)

                # Convert resolutions back to the original format
                self.resolutions = [f"{res}p" for res in self.resolutions]

            else:
                self.conn = False
        except Exception as e:
            print(f"there is an error {e}")



    def download(self,res,path):
        try:
            # get the video with the wished resolution
            self.yd = self.yt.streams.get_by_resolution(resolution=res)

            if self.yd:
                # download the video in a specific path
                self.yd.download(output_path=path)
                return True
            else:
                return False
        except Exception as e:
            return f"error {e}"



if __name__ == "__main__":
    url = input("video url: ")
    Downloader(url)
