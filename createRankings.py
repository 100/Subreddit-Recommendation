import sqlite3
import numpy
import scipy.spatial.distance
import json

def fetchTopSubreddits(topXSkip, limit):
    conn = sqlite3.connect("database.sqlite")
    results = conn.execute("""SELECT DISTINCT subreddit, COUNT(*) as count
        FROM MAY2015 GROUP BY subreddit ORDER BY count DESC""")
    subreddits = {}
    for subreddit, count in results[topXSkip: topXSkip + limit]:
        subreddits[subreddit] = count
    conn.close()
    return subreddits

def fetchUsers():
    conn = sqlite3.connect("database.sqlite")
    users = []
    for user in conn.execute("""SELECT DISTINCT author from MAY2015"""):
        users.append(user)
    conn.close()
    return users

def mapUserVectors(topSubreddits, users):
    conn = sqlite.connect("database.sqlite")
    subredditVectors = {}
    dbData = conn.execute("""SELECT subreddit, author FROM MAY2015""")
    for subreddit, user in dbData:
        if subreddit in subredditVectors:
            if subreddit in topSubreddits and user in users:
                subredditVectors[subreddit][users.index(user)] = 1
        else:
            subredditVectors[subreddit] = [0] * len(users)
    con.close()
    return subredditVectors

def createVectorsMatrix(subredditVectors):
    matrix = numpy.array(subredditVectors.values())
    return matrix

def createDistanceMatrix(subredditVectors, vectorsMatrix):
    matrix = numpy.zeros((len(subredditVectors), len(subredditVectors)))
    distances = pdist(vectorsMatrix, "jaccard")
    return distances

def createRankingsJSON(subredditVectors, distanceMatrix, topXSubs):
    jsonDistances = {}
    for subreddit in subredditVectors:
        idx = subredditVectors.keys().index(subreddit)
        row = list(distanceMatrix[idx])
        names = [sub for idx, sub in enumerate(subredditVectors.keys()) if row[idx] != 0]
        sortedNames = sorted(names, reverse = True, key = lambda x: row[subredditVectors.keys().index(x)])
        jsonDistances[subreddit] = sortedNames[0: topXSubs]
    with open("distanceMatrix.json", "w") as matrix:
        json.dumps(jsonDistances, matrix)
