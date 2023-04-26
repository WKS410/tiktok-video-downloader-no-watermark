import argparse
import requests
import signal
import sys
import os
import coloredlogs
import logging
from tqdm import tqdm


# Define service
SERVICE = 'TIKTOK'

# Logger settings
LOG_FORMAT = "%(asctime)s - [{level[0]}] - {service} - %(message)s".format(level="levelname", service=SERVICE)
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
coloredlogs.install(level='INFO', fmt=LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
logger = logging.getLogger(SERVICE)


def download_video(url, filename):
        # Start downloading video
    logging.info("Downloading video...")
    response = requests.get(url, stream=True)

    # obtiene el tamaño del archivo a descargar en bytes
    file_size = int(response.headers.get('Content-Length', 0))

    # crea una instancia de tqdm
    progress_bar = tqdm(total=file_size, unit='B', unit_scale=True, desc=f'Downloading {filename}')

    with open(filename, 'wb') as file:
        for data in response.iter_content(chunk_size=1024):
            # escribe los datos del archivo en el disco
            file.write(data)

            # actualiza el indicador de progreso
            progress_bar.update(len(data))

            # verifica si se ha recibido una señal de interrupción
            if stop_signal:
                break

    # cierra la instancia de tqdm
    progress_bar.close()


def sigint_handler(signal, frame):
    global stop_signal
    stop_signal = True


if __name__ == '__main__':
    # registra el manejador de señal SIGINT
    signal.signal(signal.SIGINT, sigint_handler)

    # analiza los argumentos de la línea de comandos
    parser = argparse.ArgumentParser(description='Download a TikTok video file using tqdm.')
    parser.add_argument('-id', '--input-id', dest='input_id', help='ID of the video file to download.')
    parser.add_argument('-i', '--input-url', dest='input_url', help='URL of the live video file to download.')
    args = parser.parse_args()

    # indica que no se ha recibido una señal de interrupción
    stop_signal = False

    if args.input_id:
        # descarga el video normal
        url = f'https://tikwm.com/video/media/hdplay/{args.input_id}.mp4'
        filename = f'{args.input_id}_TikTok.mp4'

        try:
            # descarga el archivo de video
            download_video(url, filename)
        except KeyboardInterrupt:
            # interrupción por teclado
            logger.info('Download interrupted.')
            sys.exit(0)

        logger.info('Download completed.')

    elif args.input_url:
        # descarga el live
        url = args.input_url
        filename = 'live_tiktok.mp4'

        try:
            # descarga el archivo de video
            download_video(url, filename)
        except KeyboardInterrupt:
            # interrupción por teclado
            logger.info('Download interrupted.')
            sys.exit(0)

        logger.info('Download completed.')

    else:
        logger.error('Please specify an ID or URL.')