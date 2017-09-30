import mistune
import sqlite3
import time
from datetime import datetime

def make_date(unixtime, time_format):
    return datetime.fromtimestamp(unixtime).strftime(time_format)

def get_articles(dbname, time_format):
    dbconn = sqlite3.connect(dbname)
    db = dbconn.cursor()
    db.row_factory = sqlite3.Row

    articles = list(db.execute("select * from articles"))

    for article in articles:
        article["date"] = make_date(article["date"], time_format)

    return articles
