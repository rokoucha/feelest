# -*- coding: utf-8 -*-

import configparser
from flask import Flask, render_template, request, redirect, url_for

import controller

config = configparser.ConfigParser()
config.read('config/feelest.ini', encoding="utf-8")

app = Flask("feelest")

@app.route('/')
def index():
    articles = controller.get_articles(config)
    return render_template('index.tmpl', blog=config["blog"], articles=articles)

@app.route('/article/<string:id>')
def article(id):
    if controller.exist_article(id, config):
        article_data = dict(controller.get_article(id, config))
        return render_template('article.tmpl', blog=config["blog"], article=article_data, is_article=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
