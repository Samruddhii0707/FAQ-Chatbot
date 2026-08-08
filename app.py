from flask import Flask, request, jsonify, send_from_directory
import os
from flask import Flask, request, jsonify
import re

import nltk

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.metrics.pairwise import cosine_similarity


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)


# --------------------------------
# NLTK SETUP
# --------------------------------

try:

    STOP_WORDS = set(
        stopwords.words("english")
    )

except LookupError:

    nltk.download("stopwords")

    STOP_WORDS = set(
        stopwords.words("english")
    )


stemmer = PorterStemmer()


# --------------------------------
# FAQ DATA
# --------------------------------

faqs = [

    (
        "what is codealpha",

        "CodeAlpha is a software development company "
        "that provides internship opportunities and "
        "practical projects."
    ),


    (
        "what are the ai tasks",

        "The AI tasks include Language Translation Tool, "
        "Chatbot for FAQs, Music Generation with AI, "
        "and Object Detection and Tracking."
    ),


    (
        "how many tasks should i complete",

        "According to the internship instructions, "
        "you need to complete at least 2 or 3 tasks "
        "from the available AI task list."
    ),


    (
        "what is nltk",

        "NLTK is a Python library used for Natural "
        "Language Processing. It can be used for "
        "cleaning and processing text."
    ),


    (
        "where do i upload my code",

        "Upload your complete source code to GitHub "
        "in a repository named CodeAlpha_ProjectName."
    ),


    (
        "will i get a certificate",

        "You need to complete the minimum required "
        "tasks to be eligible for the internship certificate."
    ),


    (
        "what is chatbot",

        "A chatbot is a software application that "
        "communicates with users and provides answers "
        "to their questions."
    )

]


# --------------------------------
# TEXT PREPROCESSING
# --------------------------------

def clean_text(text):

    text = text.lower()

    text = re.sub(
        r"[^a-zA-Z\s]",
        " ",
        text
    )

    words = text.split()


    words = [

        stemmer.stem(word)

        for word in words

        if word not in STOP_WORDS

    ]


    return " ".join(words)


# --------------------------------
# PREPARE FAQ DATA
# --------------------------------

questions = [

    clean_text(question)

    for question, answer in faqs

]


# --------------------------------
# TF-IDF
# --------------------------------

vectorizer = TfidfVectorizer()

faq_vectors = vectorizer.fit_transform(
    questions
)


# --------------------------------
# GET BEST ANSWER
# --------------------------------

def get_answer(user_question):

    cleaned_question =clean_text(user_question)


    if not cleaned_question.strip():

        return (
            "Please type a question "
            "so I can help you. 😊"
        )


    user_vector =vectorizer.transform(
            [cleaned_question]
        )


    similarity_scores =cosine_similarity(
            user_vector,
            faq_vectors
        )[0]


    best_index =similarity_scores.argmax()


    best_score =similarity_scores[best_index]


    if best_score < 0.20:

        return (
            "Sorry, I don't have an answer "
            "for that yet. Try asking about "
            "CodeAlpha, AI tasks, NLTK, "
            "GitHub or certificate."
        )


    return faqs[best_index][1]

@app.route("/")
def home():
    return send_from_directory(BASE_DIR, "index.html")


@app.route("/style.css")
def style():
    return send_from_directory(BASE_DIR, "style.css")


@app.route("/script.js")
def script():
    return send_from_directory(BASE_DIR, "script.js")

# --------------------------------
# API
# --------------------------------

@app.route(
    "/chat",
    methods=["POST"]
)
def chat():

    data =request.get_json()


    message =data.get(
            "message",
            ""
        )


    answer = get_answer(message)


    return jsonify({

        "reply": answer

    })


# --------------------------------
# START SERVER
# --------------------------------

if __name__ == "__main__":

    app.run(debug=True)
    