import logging
import coloredlogs
import requests
import subprocess
import os
import argparse
from bs4 import BeautifulSoup
from tqdm import tqdm

# Define service
SERVICE = 'TIKTOK'

# Logger settings
LOG_FORMAT = "%(asctime)s - [{level[0]}] - {service} - %(message)s".format(level="levelname", service=SERVICE)
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
coloredlogs.install(level='INFO', fmt=LOG_FORMAT, datefmt=LOG_DATE_FORMAT)

# TikTok API Headers
headers = {
    'Accept': '*/*',
    'Accept-Language': 'es-ES,es;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json; charset=UTF-8',
    'Origin': 'https://www.tiktok.com',
    'Referer': 'https://www.tiktok.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

class TikTokDownloader:
    def __init__(self, video_id):
        self.video_id = video_id
        self.video_url = f"https://tikwm.com/video/media/hdplay/{video_id}.mp4"

    def download_video(self):
        # Start downloading video
        logging.info("Downloading video...")
        r = requests.head(self.video_url, allow_redirects=True)
        total_size = int(r.headers.get('content-length', 0))
        block_size = 1024
        t=tqdm(total=total_size, unit='iB', unit_scale=True)
        with requests.get(self.video_url, stream=True) as r:
            r.raise_for_status()
            with open(f"{self.video_id}_TikTok.mp4", 'wb') as f:
                for chunk in r.iter_content(chunk_size=block_size):
                    if chunk:
                        f.write(chunk)
                        t.update(len(chunk))
        t.close()
        logging.info("Video downloaded successfully!")
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-id", "--id", dest="id_tiktok", help="Url Tiktok", required=True)
    args = parser.parse_args()
    video_id = str(args.id_tiktok) 

    downloader = TikTokDownloader(video_id)
    downloader.download_video()