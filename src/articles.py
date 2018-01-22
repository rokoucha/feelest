from datetime import datetime
import mistune

def get_articles(DB, invisible, timeformat, url):
    """
    Get article list from DB
    """
    articles = []

    sql = "select * from articles where invisible=? order by unixtime DESC"

    for row in list(DB.execute(sql, (str(1 if invisible else 0)))):
        article = dict(row)
        article["date"] = datetime.fromtimestamp(row["unixtime"]).strftime(timeformat)
        article["url"] = url + "/article/" + str(row["id"])
        articles.append(row)

    return articles

def get_article(DB, articleid, invisible, timeformat, url):
    """
    Get article use article id from DB
    """
    article = {}

    sql = "select * from articles where id=? and invisible=?"

    for row in list(DB.execute(sql, (articleid, str(1 if invisible else 0)))):
        article = dict(row)
        article["date"] = datetime.fromtimestamp(article["unixtime"]).strftime(timeformat)
        article["url"] = url + "/article/" + str(article["id"])

    return article

def exist_article(DB, articleid, invisible):
    """
    Check exist article in DB
    """

    sql = "select * from articles where id=? and invisible=?"

    return True if DB.execute(sql, (articleid, 1 if invisible else 0)) != "" else False
