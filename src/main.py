# -*- coding: utf-8 -*-

import configparser
from flask import Flask, render_template, redirect, request, session
from flask_httpauth import HTTPDigestAuth
import sqlite3
import tweepy

import controller

config = configparser.ConfigParser()
config.read("config/feelest.ini", encoding="utf-8")

app = Flask("feelest")

@app.route("/")
def index():
    articles = controller.get_articles(invisible=True, config=config)
    return render_template("index.tmpl", blog=config["blog"], articles=articles)

@app.route("/article/<string:id>")
def article(id):
    if controller.exist_article(id=id, invisible=True, config=config):
        article_data = dict(controller.get_article(id=id, invisible=True, config=config))
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
