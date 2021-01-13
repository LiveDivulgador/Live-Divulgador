from sqlalchemy import create_engine, MetaData, Column
from sqlalchemy.types import Boolean
import pandas as pd
import os

engine = create_engine("postgres://{}:{}@localhost:5432/streamers".format(os.getenv("user_db"), os.getenv("passwd_db")))

# Caso a tabela não exista, vamos criá-la
engine.execute("CREATE TABLE IF NOT EXISTS livecoders (Nome varchar(50), Id integer,\
	Twitch varchar(150), Twitter varchar(50), OnStream boolean, Print boolean,\
	Tipo varchar(5))")

# Guardar objeto da table livecoders
metadata = MetaData(bind=engine, reflect=True)

livecoders = metadata.tables["livecoders"]


def returnStreamerInfo():

	# Retonar as os valores das colunas de todos os streamers
	result = engine.execute("SELECT * FROM livecoders")

	return result

def returnStreamerNames():

	# Retorna o nome dos streamers
	result = engine.execute("SELECT Nome FROM livecoders")

	return result

def insertStreamers(streamers):

	# Insere novos streamers na DB
	for index, row in streamers.iterrows():
		ins = livecoders.insert()\
		.values(nome=row["Nome"], id=int(row["Id"]), twitch=row["Twitch"],
			twitter=row["Twitter"], onstream=row["OnStream"], print=row["Print"],
			tipo=row["Tipo"])
		
		engine.execute(ins)

	return

def insertOnStream(idt, value):
	# Atribui true ou false à coluna OnStream
	upd = livecoders.update().values(onstream=value).where(livecoders.c.id==idt)
	engine.execute(upd)

	return


def updateName(idt, name, twitch):
	""" Função que atualizar o nome e o link com base no id"""
	
	# Atualizar nome
	upd = livecoders.update().values(nome=name, twitch=twitch).where(livecoders.c.id==idt)
	engine.execute(upd)

	return

def deleteStreamer(idt):

	""" Função que elimina streamer da DB com base no id"""
	delete = livecoders.delete().where(livecoders.c.id==int(idt))
	engine.execute(delete)

	return
