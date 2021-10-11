# Pacotes de terceiros
import os
import threading
import time

import schedule
from dotenv import load_dotenv

# Preparar o env
load_dotenv()

from db import insert_on_stream, return_streamer_info
from tt import tweet
from twitch import (
    get_OAuth,
    get_stream_title,
    get_streamer_name,
    is_streamer_live,
)
from utils import remove_cmds_from_title

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
    results = return_streamer_info().fetchall()

    # Iterar streamers
    for streamer in results:

        # ID Twitch
        idt = streamer[1]

        # Verificar se está em live e retornar categoria a streamar
        is_live, category = is_streamer_live(idt, header)

        # Verificar se:
        # 1 - Está online
        # 2 - Está numa categoria permitida
        if is_live and category in categories:

            # Verificar se ele já estava live antes (na base de dados)
            is_live = streamer[4]

            # if not is_live and db.streamer_timeout(idt):
            if not is_live:

                # Titulo da live
                title = get_stream_title(idt, header)

                # Remover comandos do título
                title = remove_cmds_from_title(title)

                # Obter o URL atualiazado do canal
                twitch, name = get_streamer_name(idt, header)

                # Informações do streamer vindas da base de dados
                twitter = streamer[3]
                is_print = streamer[5]
                streamer_type = streamer[6]
                hashtags = streamer[7]

                # Como está em live, vamos deixar verdadeiro na base de dados
                insert_on_stream(idt, True)

                # Vamos fazer o tweet
                tweet(
                    idt,
                    name,
                    twitch,
                    twitter,
                    title,
                    is_print,
                    streamer_type,
                    category,
                    hashtags,
                )
        else:
            # Caso não esteja em live, definir como falso
            insert_on_stream(idt, False)


def threaded_job(job):
    # Função para correr a main em modo threading
    thread = threading.Thread(target=main)
    thread.start()

    # Esperar pela thread terminar
    thread.join()


if __name__ == "__main__":

    schedule.every(60).seconds.do(threaded_job, main)

    while True:
        schedule.run_pending()

        # Performance measure
        time.sleep(30)
