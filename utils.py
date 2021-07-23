import os
import sys
import pandas as pd
import time
import requests
import shutil
from PIL import Image

# Caminho absoluto deste ficheiro
ABS_PATH = os.path.abspath(__file__)

# Caminho desta pasta
DIR_PATH = os.path.dirname(ABS_PATH)

# Caminho desta pasta + o ficheiro que eu quero acessar
FILE = os.path.join(DIR_PATH, "streamers.csv")


def read_streamers():
    # Ler os nomes dos streamers de um .csv
    if os.path.exists(FILE):

        try:
            df = pd.read_csv(FILE, sep=",", encoding="latin-1")
            return df
        except:
            # Retornar um dataframe vazio, caso o ficheiro esteja vazio
            return pd.DataFrame({})
    else:
        print("O ficheiro " + FILE + " não existe!")
        sys.exit(1)


def delete_exist_streamers(streamers, names):
    # Eliminar Streamers que já estão na BD
    for name in names:
        i = streamers[streamers["Nome"] == name].index
        streamers = streamers.drop(i)

    return streamers


def remove_cmds_from_title(title):

    # Função que remove os comandos colocados nos títulos
    # apenas por uma questão de objetividade no título
    arr = title.split()

    output = " ".join(list(filter(lambda x: x[0] != "!", arr)))

    return output


def get_image(name):

    # Função que faz download da imagem da stream
    url = f"https://static-cdn.jtvnw.net/previews-ttv/live_user_{name}-1280x720.jpg"

    img_name = name + ".jpg"

    r = requests.get(url, stream=True)

    if r.status_code == 200:

        # Isto para que o tamanho do download não seja 0
        r.raw.decode_content = True

        with open(img_name, "wb") as fw:
            # Escrever a imagem no disco
            shutil.copyfileobj(r.raw, fw)

        # Converter a imagem para .png
        img = Image.open(img_name)

        img.save(name + ".png")

        return name, True

    return None, False


def update_csv(streamers):
    """Função encarregue de guardar as modificações num .csv"""
    os.remove(FILE)
    streamers.to_csv(FILE, sep=",", index=False)

    return
