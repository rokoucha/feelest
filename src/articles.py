from datetime import datetime
from mistune import markdown

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

def get_unique(db):
    """
    Get unique article id
    """

    ids = "select id from articles order by id DESC"

    return [str(row[0]) for row in db.execute(ids)]

def add_article(db, author, title, description, tag, md, invisible):
    """
    Add article from markdown file
    """

    add = "insert into articles values(?,\"?\",\"?\",\"?\",\"?\",\"?\",\"?\",\"?\",?)"

    newid = get_unique(db) + 1
    html = markdown(md)
    unixtime = datetime.now().strftime('%s')

    return db.execute(add, (
        newid,
        author,
        title,
        description,
        unixtime,
        tag,
        md,
        html,
        invisible
    ))

def update_article(db, articleid, author="", title="", unixtime="", description="", tag="", md="", invisible=""):
    """
    Update aritlce
    """

    updates = ""

    if author != "":
        updates += "author = \"{}\",".format(author)
    if title != "":
        updates += "title = \"{}\",".format(title)
    if unixtime != "":
        updates += "unixtime = {},".format(unixtime)
    if description != "":
        updates += "description = \"{}\",".format(description)
    if tag != "":
        updates += "tag = \"{}\",".format(tag)
    if md != "":
        updates += "markdown = \"{}\",".format(md)
    if invisible != "":
        updates += "markdown = \"{}\",".format(md)

    update = "insert into articles values(?) where id=?"

    return db.execute(update, (updates.rstrip(","), articleid))

def delete_article(db, articleid):
    """
    Delete article
    """

    delete = "delete from articles where id=?"

    return db.execute(delete, (articleid))
