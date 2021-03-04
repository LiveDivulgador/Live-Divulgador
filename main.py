import db
from twitch import getOAuth, isStreamerLive, nameChanged, getStreamTitle, getStreamerId
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

    # Definir tokens e header
    access_token, header = getOAuth()

    # DataFrame com os dados dos streamers
    streamers = readStreamers()

    # Se não estiver vazio vamos pegar os IDs
    if not streamers.empty:
        # Verificar se o streamer está registado na DB
        results = db.returnStreamerNames().fetchall()

        # Guardar o nome dos streamers já registados
        names = []
        for r in results:
            names.append(*r)

        # Retorno de todos os streamers que não estão na BD
        streamers = deleteExistStreamers(streamers, names)

        # Retornar o dataframe com o id de cada novo streamer
        streamers = getStreamerId(streamers, header)

        # Inserir cada streamer na BD
        db.insertStreamers(streamers)

        if names:
            # DataFrame com os dados dos streamers
            streamers = readStreamers()

            # Retornar todas as infos dos streamers na DB
            results = db.returnStreamerInfo().fetchall()

            # Preencher o dataframe com os Ids
            for streamer in results:
                name = streamer[0]
                idt = streamer[1]

                index = streamers[streamers["Nome"] == str(name)].index
                streamers.loc[index, "Id"] = str(idt)

            # Antes de tudo vamos verificar se algum streamer
            # trocou o nome do canal

            # print(streamers)
            streamers, modified = nameChanged(streamers, header)

        if modified:
            # Guardar alterações no .csv
            updateCSV(streamers)

            # Ler novamente
            streamers = readStreamers()

        results = db.returnStreamerInfo().fetchall()

        # Verificar se o streamer está em live ou não
        for streamer in results:
            idt = streamer[1]

            if isStreamerLive(str(idt), header):
                title = getStreamTitle(idt, header)

                # Remover comandos do título
                title = removeCmdsFromTitle(title)

                # Verificar se ele já estava live antes
                # se sim não fazemos outra vez o tweet
                # se não fazemos o tweet
                is_live = streamer[4]

                if not is_live:
                    twitch = streamer[2]
                    twitter = streamer[3]
                    isPrint = streamer[5]
                    streamer_type = streamer[6]
                    hashtags = streamer[7]

                    # Vamos fazer o tweet
                    db.insertOnStream(idt, True)
                    tweet(twitch, twitter, title,
                          isPrint, streamer_type, hashtags)

            else:
                db.insertOnStream(idt, False)

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
