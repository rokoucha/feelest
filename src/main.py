# -*- coding: utf-8 -*-

from configparser import ConfigParser
from flask import Flask, render_template, redirect, request, session
from flask_httpauth import HTTPDigestAuth
import sqlite3
import tweepy

import articles
import auth

CONFIG = ConfigParser()
CONFIG.read("config/feelest.ini", encoding="utf-8")

APP = Flask("feelest")

dbconnector = sqlite3.connect("database/" + CONFIG["system"]["dbname"])
dbcursor = dbconnector.cursor()
dbconnector.row_factory = sqlite3.Row

@APP.route("/")
def index():
    """
    Return index page
    """
    article_list = articles.get_articles(invisible=True, config=CONFIG)
    return render_template("index.tmpl", blog=CONFIG["blog"], articles=article_list)

@APP.route("/article/<string:id>")
def article(id):
    """
    Return article page
    """
    if articles.exist_article(id=id, invisible=True, config=CONFIG):
        article_data = dict(articles.get_article(id=id, invisible=True, config=CONFIG))
        return render_template("article.tmpl", blog=CONFIG["blog"], article=article_data, is_article=True)

@APP.route("/login", methods=["GET", "POST"])
def login():
    """
    Login with digest or oauth
    """
    if request.method == "POST":
        if CONFIG["system"]["authenticator"] == "digest":
            session["username"] = request.form["username"]
            return redirect(request.referrer or "/")
    return render_template("login.tmpl")

@APP.route("/logout")
def logout():
    """
    Logout from feelest
    """
    session.pop("session_token", None)
    return redirect(request.referrer or "/")

if __name__ == "__main__":
    APP.run(host="0.0.0.0")
