import os
import sys
import pandas as pd
import requests
import shutil
import logging
from PIL import Image

# Configuração para criar logs deste ficheiro
log = logging.getLogger("utils-log")
log.setLevel(logging.DEBUG)
fh = logging.FileHandler('utils.log')
fh.setLevel(logging.DEBUG)
log.addHandler(fh)

# Caminho absoluto deste ficheiro
DIR_PATH = os.path.abspath(os.path.dirname("../../"))

# Caminho desta pasta + o ficheiro que eu quero acessar
FILE = os.path.join(DIR_PATH, "streamers.csv")


def read_streamers():
    """
    NOTA: Precisa ser removida no futuro

    Ler os nomes dos streamers de um .csv
    """

    if os.path.exists(FILE):

        try:
            df = pd.read_csv(FILE, sep=",", encoding="latin-1")
            return df
        except FileNotFoundError:
            # Retornar um dataframe vazio, caso o ficheiro esteja vazio
            return pd.DataFrame({})
    else:
        print("O ficheiro " + FILE + " não existe!")
        sys.exit(1)


def delete_exist_streamers(streamers, names):

    """
    NOTA: Precisa ser removida no futuro

    Eliminar Streamers que já estão na BD
    """

    for name in names:
        i = streamers[streamers["Nome"] == name].index
        streamers = streamers.drop(i)

    return streamers


def remove_cmds_from_title(title):

    """
    Função que remove os comandos colocados nos títulos
    apenas por uma questão de objetividade no título
    """

    arr = title.split()

    output = " ".join(list(filter(lambda x: x[0] != "!", arr)))

    return output


def get_image(name, dir):

    """
    Função que obtém a imagem para anexar ao tweet
    """

    url = f"https://static-cdn.jtvnw.net/previews-ttv/live_user_{name}-1280x720.jpg"

    img_name = name + ".jpg"
    img_name = os.path.join(dir, img_name)

    r = requests.get(url, stream=True)
    log.debug(
        "[!] Func: get_image - Status: %s - Streamer: %s"
        % (r.status_code, name)
    )

    if r.status_code == 200:

        # Isto para que o tamanho do download não seja 0
        r.raw.decode_content = True

        with open(img_name, "wb") as fw:
            # Escrever a imagem no disco
            shutil.copyfileobj(r.raw, fw)

        # Converter a imagem para .png
        img = Image.open(img_name)

        img.save(os.path.join(dir, name + ".png"))

        return name, True

    return None, False


def update_csv(streamers):

    """
    NOTA: Esta função será eliminada no futuro

    Função encarregue de guardar as modificações num .csv
    """

    os.remove(FILE)
    streamers.to_csv(FILE, sep=",", index=False)

    return
