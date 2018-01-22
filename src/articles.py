import mistune
import sqlite3
import time
from datetime import datetime

def get_articles(invisible, config):
    dbname = "database/" + config["system"]["dbname"]
    url = config["blog"]["url"]
    time_format = config["system"]["time_format"]

    dbconn = sqlite3.connect(dbname)
    db = dbconn.cursor()
    db.row_factory = sqlite3.Row

    articles = []

    for rowt in list(db.execute("select * from articles where invisible=? order by unixtime DESC", (str(1 if invisible else 0)))):
        row = dict(rowt)
        row["date"] = datetime.fromtimestamp(row["unixtime"]).strftime(time_format)
        row["url"] = url + "/article/" + str(row["id"])
        articles.append(row)

    return articles

def get_article(id, invisible, config):
    dbname = "database/" + config["system"]["dbname"]
    url = config["blog"]["url"]
    time_format = config["system"]["time_format"]

    dbconn = sqlite3.connect(dbname)
    db = dbconn.cursor()
    db.row_factory = sqlite3.Row

    article = {}

    for row in list(db.execute("select * from articles where id=? and invisible=?", (id, str(1 if invisible else 0)))):
        article = dict (row)
        article["date"] = datetime.fromtimestamp(article["unixtime"]).strftime(time_format)
        article["url"] = url + "/article/" + str(article["id"])

    return article

def exist_article(id, invisible, config):
    dbname = "database/" + config["system"]["dbname"]

    dbconn = sqlite3.connect(dbname)
    db = dbconn.cursor()
    db.row_factory = sqlite3.Row

    return True if db.execute("select * from articles where id=? and invisible=?", (id, 1 if invisible else 0)) != "" else False
