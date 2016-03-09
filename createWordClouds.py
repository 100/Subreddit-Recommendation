import sqlite3
from sklearn.feature_extraction.text import CountVectorizer
import json

def createWordsJSON(numWords, subreddits):
    print "Creating word clouds JSON...\n"
    conn = sqlite3.connect("database.sqlite")
    subredditWords = {}
    completed = 0
    for subreddit in subreddits:
        results = conn.execute("""SELECT subreddit, body FROM MAY2015 WHERE subreddit=?""", (subreddit,))
        comments = []
        for subreddit, comment in results:
            comments.append(preprocess(comment))
        counter = CountVectorizer(stop_words = "english", lowercase = True, max_features = numWords)
        counts = counter.fit_transform(comments)
        subredditWords[subreddit] = counts
        completed += 1
        if completed % 1000 == 0:
            print "\tProcessed %s subreddits...\n" % (completed)
    conn.close()
    with open("wordClouds.json", "w") as clouds:
        json.dumps(subredditWords, clouds)


def preprocess(comment):
    lowered = comment.lower()
    strippedPunct = lower.translate(string.maketrans("", ""), string.punctuation)
    acceptable = string.digits + string.letters
    cleansedList = []
    for word in strippedPunct.split():
        boolAcceptables = [char in acceptable for char in word]
        if False in boolAcceptables:
            continue
        else:
            cleansedList.append(word)
    return " ".join(cleansedList)
