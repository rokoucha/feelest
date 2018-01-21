# -*- coding: utf-8 -*-

import configparser
from flask import Flask, render_template, redirect, session
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

@app.route("/login/twitter")
def login():
    auth = tweepy.OAuthHandler(config["oauth"]["consumer_key"], config["oauth"]["consumer_secret"], config["blog"]["url"]+"/login/twitter/callback")
    redirect_url = auth.get_authorization_url()
    session["request_token"] = auth.request_token
    return redirect(redirect_url)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
