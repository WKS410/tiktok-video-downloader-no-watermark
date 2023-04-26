import argparse
import requests
import signal
import sys
import os
import coloredlogs
import logging
from tqdm import tqdm
from urllib.parse import urlparse, urlunparse


# Define service
SERVICE = 'TIKTOK'

# Logger settings
LOG_FORMAT = "%(asctime)s - [{level[0]}] - {service} - %(message)s".format(level="levelname", service=SERVICE)
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
coloredlogs.install(level='INFO', fmt=LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
logger = logging.getLogger(SERVICE)

def check_link(url):
    """
    Comprueba si un enlace es accesible.

    :param url: str, la dirección URL del enlace a comprobar
    :return: bool, True si el enlace es accesible, False en caso contrario
    """
    try:
        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            # La URL es inválida si no tiene un esquema o dominio
            return False
        # Reensamblar la URL para evitar problemas de codificación
        url = urlunparse(parsed_url)
        response = requests.head(url, timeout=5)
        return response.status_code == 200
    except (requests.ConnectionError, requests.Timeout):
        return False

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
    parser.add_argument('-id', '--input-id', dest='input_id_normal', help='ID of the video file to download.')
    parser.add_argument('-url', '--input-url', help='URL del enlace a comprobar')
    args = parser.parse_args()

    # indica que no se ha recibido una señal de interrupción
    stop_signal = False

    if args.input_id_normal:
        # descarga el video normal
        url = f'https://tikwm.com/video/media/hdplay/{args.input_id_normal}.mp4'
        filename = f'{args.input_id_normal}_TikTok.mp4'

        try:
            # descarga el archivo de video
            download_video(url, filename)
        except KeyboardInterrupt:
            # interrupción por teclado
            logger.info('Download interrupted.')
            sys.exit(0)

        logger.info('Download completed.')

    elif args.input_url:
            # Extraer el ID de la URL
        parsed_url = urlparse(args.input_url)
        filename = parsed_url.path.split('/')[-1]
        id = filename.split('_')[0][7:]
            # Construir las URLs con el ID
        url_or4 = f'https://pull-flv-l11-va01.tiktokcdn.com/stage/stream-{id}_or4.flv'
        url_ld = f'https://pull-flv-l11-va01.tiktokcdn.com/stage/stream-{id}_ld.flv'
        url_sd = f'https://pull-flv-l11-va01.tiktokcdn.com/stage/stream-{id}_sd.flv'
        url_hd = f'https://pull-flv-l11-va01.tiktokcdn.com/stage/stream-{id}_hd.flv'
        url_uhd = f'https://pull-flv-l11-va01.tiktokcdn.com/stage/stream-{id}_uhd.flv'
        # descarga el live
        option = input("Select an option (1-6):\n1. url_or4\n2. url_ld\n3. url_sd\n4. url_hd\n5. url_uhd\n")
        if option == '1':
            url = url_or4
        elif option == '2':
            url = url_ld
        elif option == '3':
            url = url_sd
        elif option == '4':
            url = url_hd
        elif option == '5':
            url = url_uhd
        else:
            logger.error('Opción no válida')
            exit(1)

        if check_link(url):
            
            filename = f'{id}_Live_Tiktok.mp4'
            try:
                
                # descarga el archivo de video
                download_video(url, filename)
            except KeyboardInterrupt:
                # interrupción por teclado
                logger.info('Download interrupted.')
                sys.exit(0)

            logger.info('Download completed.')
        else:
            logger.error('Please specify a valid URL.')