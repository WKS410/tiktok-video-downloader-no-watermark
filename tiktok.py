import requests
import subprocess
import os
import argparse
import requests
from bs4 import BeautifulSoup
from progress.bar import ShadyBar


arguments = argparse.ArgumentParser()
arguments.add_argument("-id", '--id', dest="id_tiktok", help="Url Tiktok", required=True)
args = arguments.parse_args()

id_tiktok = str(args.id_tiktok) 

currentFile = __file__
realPath = os.path.realpath(currentFile)
dirPath = os.path.dirname(realPath)
dirName = os.path.basename(dirPath)
dir = dirPath

aria2cexe = dirPath + '/aria2c.exe'

By = ([f"By watora#1588 and -∞WKS∞-#3982"])
print(f'{By}')
headers = {
    'Accept': '*/*',
    'Accept-Language': 'es-ES,es;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json; charset=UTF-8','Origin': 'https://www.tiktok.com',
    'Referer': 'https://www.tiktok.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

HEADERSUWU = ([f"{headers}"])
print(f'{HEADERSUWU}')

DOWNLOADING = ([f"[+] DOWNLOADING..."])
print(f'{DOWNLOADING}')
video_url = "https://tikwm.com/video/media/hdplay/" + id_tiktok + ".mp4"
r = requests.head(video_url, allow_redirects=True)
subprocess.run([aria2cexe,
                r.url,
                '-o', 
                f"{id_tiktok}_TikTok.mp4"])
DONE = ([f"[+] DONE"])
print(f'{DONE}')