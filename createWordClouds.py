import sqlite3
import numpy
from sklearn.feature_extraction.text import CountVectorizer
import json

def createWordVectors(numSubreddits):
    conn = sqlite3.connect(database.db)
    subreddits = {}
    results = con.execute("""SELECT subreddit, body FROM MAY2015"""):
    for subreddit, comment in results:
        if subreddit in subreddits:
            subreddits[subreddit].append(comment)
        else:
            subreddits[subreddit] = [comment]
    conn.close()
    sortedSubs = sorted(subreddits.items(), reverse = True, key = lambda x: len(x[1]))
    return dict(sortedSubs[0: numSubreddits])

def preprocess(comment):
    lowered = comment.lower()
    strippedPunct = lower.translate(string.maketrans("", ""), string.punctuation)
    acceptable = string.digits + string.letters
    cleansedList = []
    for word in strippedPunct.split():
        boolAcceptables = [char in acceptable for char in word]
        if (False in boolAcceptables):
            continue
        else:
            cleansedList.append(word)
    return " ".join(cleansedList)
