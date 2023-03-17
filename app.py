import os

import openai
from flask import Flask, redirect, render_template, request, url_for
import socks
import socket

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

# set proxy
socks.set_default_proxy(socks.SOCKS5, "localhost", 1080)
socket.socket = socks.socksocket

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        animal = request.form["animal"]
        # passage = request.form["passage"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(animal),
            # prompt=revise_prompt(passage),
            temperature=0.6,
        )
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(animal):
    return """Suggest three names for an animal that is a superhero.

Animal: Cat
Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
Animal: Dog
Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
Animal: {}
Names:""".format(
        animal.capitalize()
    )

def revise_prompt(passage):
    return """Please proofread and polish the passage from an academic angle and highlight the modification:

    {}""".format(passage)