from datetime import datetime
import mistune

def get_articles(db, invisible, timeformat, url):
    """
    Get article list from db
    """
    articles = []

    getarticle = "select * from articles where invisible=? order by unixtime DESC"

    for row in db.execute(getarticle, (str(1 if invisible else 0))):
        article = dict(row)
        article["date"] = datetime.fromtimestamp(article["unixtime"]).strftime(timeformat)
        article["url"] = url + "/article/" + str(article["id"])
        articles.append(article)

    return articles

def get_article(db, articleid, invisible, timeformat, url):
    """
    Get article use article id from db
    """
    article = {}

    getarticle = "select * from articles where id=? and invisible=?"

    for row in db.execute(getarticle, (articleid, str(1 if invisible else 0))):
        article = dict(row)
        article["date"] = datetime.fromtimestamp(article["unixtime"]).strftime(timeformat)
        article["url"] = url + "/article/" + str(article["id"])

    return article

def exist_article(db, articleid, invisible):
    """
    Check exist article in db
    """

    exist = "select id from articles where id=? and invisible=?"

    return articleid in [str(row[0]) for row in db.execute(exist, (articleid, 1 if invisible else 0))]
