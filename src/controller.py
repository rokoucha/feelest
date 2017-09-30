import mistune
import sqlite3
import time
from datetime import datetime

def get_articles(config):
    dbname = "database/" + config["system"]["dbname"]
    url = config["blog"]["url"]
    time_format = config["system"]["time_format"]

    dbconn = sqlite3.connect(dbname)
    db = dbconn.cursor()
    db.row_factory = sqlite3.Row

    articles = []

    for row in list(db.execute("select * from articles")):
        row["date"] = datetime.fromtimestamp(row["unixtime"]).strftime(time_format)
        row["url"] = url + row["name"]
        articles.append(row)

    return articles
