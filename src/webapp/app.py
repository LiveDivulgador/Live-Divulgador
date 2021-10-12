import os

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

from ..bot.twitch import get_1_streamer_id

# Preparar o env
load_dotenv()

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/get_streamer_id/")
def get_streamer_id():
    try:
        streamer_id = get_1_streamer_id(request.args.get("twitch_name"))

        # retornar json com o id
        return jsonify(id=streamer_id), 200

    # Streamer não encontrado
    except IndexError:
        # retornar json com erro
        return jsonify(msg="Streamer não encontrado"), 404


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
