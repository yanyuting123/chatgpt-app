import os
import openai
from flask import Flask, redirect, render_template, request, url_for, g
from operate_db import DBOperator
import req_gpt

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

db = DBOperator('data/data.db')

if "http_proxy" not in os.environ and "https_proxy" not in os.environ:
    os.environ["http_proxy"] = "http://127.0.0.1:7890"
    os.environ["https_proxy"] = "http://127.0.0.1:7890"

@app.before_request
def init_g():
    g.new_words = []

@app.route("/data/get_sources", methods=["POST"])
def get_sources():
    data = db.get_wordsource_list()
    return {'data': data}

@app.route("/data/get_source_data", methods=["POST"])
def get_source_data():
    message = None
    words = []
    req_data = request.json
    id_, name = req_data['id'], req_data['name']
    try:
        words = db.get_wordsource_data(id_, name)
    except Exception as e:
        message = e.args
    return {'data': words, 'message': message}

@app.route("/data/get_new_words", methods=["POST"])
def get_new_words():
    message = None
    words = []
    req_data = request.json
    id_, name, number = req_data['id'], req_data['name'], req_data['number']
    try:
        words = db.get_new_words(id_, name, number)
    except Exception as e:
        message = e.args
    g.new_words = words
    return {'data': words, 'message': message}

@app.route("/data/get_word_info", methods=["POST"])
def get_word_info():
    word = request.data.decode()
    assert word
    meaning, examples = req_gpt.word_info(word)
    return {'data': {'explanation': meaning, 'example':examples}}

@app.route("/data/get_choice_question", methods=["POST"])
def get_choice_question():
    word = request.data.decode()
    assert word
    ques, ans = req_gpt.choice_ques(word)
    return {'data': {'question': {'answer': ans, 'content': ques}}}

@app.route("/data/get_article", methods=["POST"])
def get_article():
    words = g.new_words
    article = req_gpt.article(words)
    return {'data': article}

@app.route("/data/check_answer", methods=["POST"])
def check_sentence():
    sentence = request.data.decode()
    res = req_gpt.check_sentence(sentence)
    return {'data':{'analysis': res}}

if __name__ == "__main__":
    app.run(host="0.0.0.0")

