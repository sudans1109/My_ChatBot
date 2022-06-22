# Code for Reshma's Chatbot
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
from flask import Flask, render_template, request
# import Flask
import requests
from math import sqrt

app = Flask(__name__)
# Create a new chatbot and name the chatbot SQLAdapter is the default adapter. If we do not specify any adapter,
# SQLStorageadapter is used automatically. Login Adapter: Is a list of logic adapters,It is a class that takes an-
# input statement and returns a response to that statement.
bot = ChatBot("chatbot", read_only=False,
              database_uri='sqlite:///database.sqlite3',
                preprocessors=[
                     'chatterbot.preprocessors.clean_whitespace'
                ],
              logic_adapters=[
                  {
                      "import_path": "chatterbot.logic.BestMatch",
                      "default_response": "Sorry I don't have an answer",
                  },
                  {
                      "import_path": "chatterbot.logic.MathematicalEvaluation",
                  },
                  {
                      "import_path": "chatterbot.logic.TimeLogicAdapter",
                      "maximum_similarity_threshold": 1.9
                  }
              ])
# bot = ChatBot(
#     'Math & Time Bot',
#     logic_adapters=[
#         'chatterbot.logic.BestMatch',
#         'chatterbot.logic.MathematicalEvaluation',
#         'chatterbot.logic.TimeLogicAdapter'
#     ],
#     database_uri='sqlite:///database.db'
# )

trainer = ChatterBotCorpusTrainer(bot)
trainer.train("chatterbot.corpus.english",
              "chatterbot.corpus.english.greetings",
              "chatterbot.corpus.english.conversations")


@app.route("/")
def main():
    return render_template("index.html")

@app.route("/get")
def get_chatbot_response():
    userText = request.args.get('userMessage')
    # Getting a response
    return str(bot.get_response(userText))


if __name__ == "__main__":
    app.run(debug=True)

#Sample Questions for the conversation with chatbot
#Hi
#Hello
#How are you?
#how do you feel
#what is soccer
#what is 2 + 2
#what is the time now?

