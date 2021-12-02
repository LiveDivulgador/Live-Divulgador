from enum import Enum
from os import getcwd

from yaml import FullLoader, load

with open(getcwd() + "/livedivulgador/twitter/message.yml", "r") as file:
    stream = file.read()
    data = load(stream, Loader=FullLoader)


class Message(Enum):
    PROTOTYPE = data["message"]
    TAGS = data["tags"]
