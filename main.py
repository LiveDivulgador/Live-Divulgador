import db
from twitch import (
    get_OAuth,
    is_streamer_live,
    name_changed,
    get_stream_title,
    get_streamer_id,
)
from tt import *
from utils import *
import time
import schedule
import threading

from dotenv import load_dotenv

load_dotenv()


def main():
    # Variável que controla se o houve
    # modificações no dados do streamer
    modified = False

    # Lista das categorias permitidas
    categories = ["Art", "Science & Technology", "Makers & Crafting"]

    # Definir tokens e header
    access_token, header = get_OAuth()

    # DataFrame com os dados dos streamers
    streamers = read_streamers()

    # Se não estiver vazio vamos pegar os IDs
    if not streamers.empty:
        # Verificar se o streamer está registado na DB
        results = db.return_streamer_names().fetchall()

        # Guardar o nome dos streamers já registados
        names = []
        for r in results:
            names.append(*r)

        # Retorno de todos os streamers que não estão na BD
        streamers = delete_exist_streamers(streamers, names)

        # Retornar o dataframe com o id de cada novo streamer
        streamers = get_streamer_id(streamers, header)

        # Inserir cada streamer na BD
        db.insert_streamers(streamers)

        if names:
            # DataFrame com os dados dos streamers
            streamers = read_streamers()

            # Retornar todas as infos dos streamers na DB
            results = db.return_streamer_info().fetchall()

            # Preencher o dataframe com os Ids
            for streamer in results:
                name = streamer[0]
                idt = streamer[1]

                index = streamers[streamers["Nome"] == str(name)].index
                streamers.loc[index, "Id"] = str(idt)

            # Antes de tudo vamos verificar se algum streamer
            # trocou o nome do canal

            # print(streamers)
            streamers, modified = name_changed(streamers, header)

        if modified:
            # Guardar alterações no .csv
            update_csv(streamers)

            # Ler novamente
            streamers = read_streamers()

        results = db.return_streamer_info().fetchall()

        # Verificar se o streamer está em live ou não
        for streamer in results:
            idt = streamer[1]

            is_live, category = is_streamer_live(str(idt), header)

            # Além de verificar se está em live, verifica se está
            # a fazer live em uma categoria permitida
            if is_live and category in categories:

                title = get_stream_title(idt, header)

                # Remover comandos do título
                title = remove_cmds_from_title(title)

                # Verificar se ele já estava live antes
                # se sim não fazemos outra vez o tweet
                # se não fazemos o tweet
                is_live = streamer[4]

                if not is_live:
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
                        hashtags,
                    )

            else:
                db.insert_on_stream(idt, False)

    else:
        print("O DataFrame está vazio!")


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
