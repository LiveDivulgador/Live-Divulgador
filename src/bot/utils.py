from os import path
import shutil
from pathlib import Path

import requests
from PIL import Image

# Diretório raiz
ROOT_DIR = str(Path(__file__).absolute().parent.parent.parent)


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

    url = f"https://static-cdn.jtvnw.net/previews-ttv/live_user_{name}\
        -1280x720.jpg"

    img_name = name + ".jpg"
    img_name = path.join(dir, img_name)

    r = requests.get(url, stream=True)

    if r.status_code == 200:

        # Isto para que o tamanho do download não seja 0
        r.raw.decode_content = True

        with open(img_name, "wb") as fw:
            # Escrever a imagem no disco
            shutil.copyfileobj(r.raw, fw)

        # Converter a imagem para .png
        img = Image.open(img_name)

        img.save(path.join(dir, name + ".png"))

        return name, True

    return None, False
