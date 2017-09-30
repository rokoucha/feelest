# -*- coding: utf-8 -*-

import configparser
from flask import Flask, render_template, request, redirect, url_for

import controller

config = configparser.ConfigParser()
config.read('config/feelest.ini')

system = config["system"]

app = Flask("feelest")

@app.route('/')
def index():
    articles = controller.get_articles("database/"+system["dbname"],system["time_format"])

    return render_template('index.html',blog=config["blog"],articles=articles)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
