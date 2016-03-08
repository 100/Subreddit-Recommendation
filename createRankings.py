import sqlite3
import numpy
import scipy.spatial.distance
import json

def fetchTopSubreddits(topXSkip, limit):
    conn = sqlite3.connect(database.db)
    subreddits = {}
    for subreddit in con.execute("""SELECT subreddit FROM MAY2015"""):
        if subreddit in subreddits:
            subreddits[subreddit] += 1
        else:
            subreddits[subreddit] = 1
    sortedSubs = sorted(subreddits.items(), reverse = True, key = lambda x: x[1])
    conn.close()
    #do not use the $topXSkip most popular, only pick $limit subreddits
    return dict(sortedSubs[topXSkip: limit + topXSkip])

def fetchUsers():
    conn = sqlite3.connect(database.db)
    users = []
    for user in con.execute("""SELECT DISTINCT author from MAY2015"""):
        users.append(user)
    conn.close()
    return users

def mapUserVectors(topSubreddits, users):
    conn = sqlite.connect(database.db)
    subredditVectors = {}
    dbData = con.execute("""SELECT subreddit, author FROM MAY2015""")
    for subreddit, user in dbData:
        if subreddit in subredditVectors:
            if subreddit in topSubreddits and user in users:
                subredditVectors[subreddit][users.index(user)] = 1
        else:
            subredditVectors[subreddit] = [] * len(users)
    con.close()
    return subredditVectors

def createVectorsMatrix(subredditVectors):
    matrix = numpy.array(subredditVectors.values())
    return matrix

def createDistanceMatrix(subredditVectors, vectorsMatrix):
    matrix = numpy.zeros((len(subredditVectors), len(subredditVectors)))
    distances = pdist(vectorsMatrix, "jaccard")
    return distances

def createJSON(subredditVectors, distanceMatrix):
    jsonDistances = {}
    for subreddit in subredditVectors:
        idx = subredditVectors.keys().index(subreddit)
        row = list(distanceMatrix[idx])
        names = [sub for idx, sub in enumerate(subredditVectors.keys()) if row[idx] != 0]
    with open("distanceMatrix.json", "w") as matrix:
        json.dumps(jsonDistances, matrix)
