# -*- coding: utf-8 -*-

from configparser import ConfigParser
from flask import Flask, render_template, redirect, request, session
from flask_httpauth import HTTPDigestAuth
import sqlite3
import tweepy

import articles
import auth

config = ConfigParser()
config.read("config/feelest.ini", encoding="utf-8")

app = Flask("feelest")

@app.route("/")
def index():
    article_list = articles.get_articles(invisible=True, config=config)
    return render_template("index.tmpl", blog=config["blog"], articles=article_list)

@app.route("/article/<string:id>")
def article(id):
    if articles.exist_article(id=id, invisible=True, config=config):
        article_data = dict(articles.get_article(id=id, invisible=True, config=config))
        return render_template("article.tmpl", blog=config["blog"], article=article_data, is_article=True)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if config["system"]["authenticator"] == "digest":
            session["username"] = request.form["username"]
            return redirect(request.referrer or "/")
    return render_template("login.tmpl")

@app.route("/logout")
def logout():
    session.pop("session_token", None)
    return redirect(request.referrer or "/")

if __name__ == "__main__":
    app.run(host="0.0.0.0")
