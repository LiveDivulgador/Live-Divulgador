# Pacotes de terceiros
import os
import threading
import time

import schedule
from dotenv import load_dotenv

# Preparar o env
load_dotenv()

# Ficheiros do bot
import db
from tt import *
from twitch import get_OAuth, get_stream_title, is_streamer_live
from utils import *

# Lista das categorias permitidas
categories = [
    "Art",
    "Science & Technology",
    "Software and Game Development",
    "Makers & Crafting",
    "Talk Shows & Podcasts",
]


def main():

    # Definir tokens e header
    access_token, header = get_OAuth()

    # Retornar dados dos streamers
    results = db.return_streamer_info().fetchall()

    # Verificar se o streamer está em live ou não
    for streamer in results:
        idt = streamer[1]

        is_live, category = is_streamer_live(str(idt), header)

        # Verificar se:
        # 1 - Está online
        # 2 - Está numa categoria permitida
        if is_live and category in categories:

            # Verificar se ele já estava live antes
            # e se não tem timeout de 3 horas
            is_live = streamer[4]

            # if not is_live and db.streamer_timeout(idt):
            if not is_live:

                title = get_stream_title(idt, header)

                # Remover comandos do título
                title = remove_cmds_from_title(title)

                twitch = streamer[2]
                twitter = streamer[3]
                is_print = streamer[5]
                streamer_type = streamer[6]
                hashtags = streamer[7]

                # Vamos fazer o tweet
                db.insert_on_stream(idt, True)

                tweet(
                    twitch,
                    twitter,
                    title,
                    is_print,
                    streamer_type,
                    category,
                    hashtags,
                )
        else:
            db.insert_on_stream(idt, False)


def threaded_job(job):
    # Função para correr a main em modo threading
    thread = threading.Thread(target=main)
    thread.start()

    # Esperar pela thread terminar
    thread.join()


if __name__ == "__main__":

    schedule.every(15).seconds.do(threaded_job, main)

    while True:
        schedule.run_pending()

        # Performance measure
        time.sleep(10)
