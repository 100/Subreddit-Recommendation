import sqlite3
import numpy
import scipy.spatial.distance
import json

def fetchTopSubreddits(topXSkip, limit):
    print "Fetching top subreddits...\n"
    conn = sqlite3.connect("database.sqlite")
    results = conn.execute("""SELECT DISTINCT subreddit, COUNT(*) as count
        FROM MAY2015 GROUP BY subreddit ORDER BY count DESC LIMIT %s""" % (limit + topXSkip))
    subreddits = {}
    currSub = 0
    for subreddit, count in results:
        if currSub < topXSkip:
            subreddits[subreddit] = count
        currSub += 1
        if currSub % 100 == 0:
            print "\tCounted %s subreddits...\n" % currSub
    conn.close()
    return subreddits

def fetchUsers():
    print "Fetching users...\n"
    conn = sqlite3.connect("database.sqlite")
    users = []
    for user in conn.execute("""SELECT DISTINCT author from MAY2015 LIMIT 50000"""):
        users.append(user)
        if len(users) % 1000 == 0:
            print "\tCounted %s users...\n" % (len(users))
    conn.close()
    usersDict = dict([(user, idx) for idx, user in enumerate(users)])
    return usersDict

def mapUserVectors(topSubreddits, users):
    print "Mapping user vectors...\n"
    conn = sqlite3.connect("database.sqlite")
    subredditVectors = {}
    dbData = conn.execute("""SELECT subreddit, author FROM MAY2015 LIMIT 5000000""")
    completed = 0
    for subreddit, user in dbData:
        if subreddit in subredditVectors:
            try:
                subredditVectors[subreddit][users[user]] = 1
            except KeyError:
                pass
        else:
            subredditVectors[subreddit] = [0] * len(users)
        completed += 1
        if completed % 1000 == 0:
            print "\tProcessed %s posts...\n" % (completed)
    conn.close()
    return subredditVectors

def createVectorsMatrix(subredditVectors):
    print "Creating vectors matrix...\n"
    matrix = numpy.array(subredditVectors.values())
    return matrix

def createDistanceMatrix(subredditVectors, vectorsMatrix):
    print "Creating distance matrix...\n"
    matrix = numpy.zeros((len(subredditVectors), len(subredditVectors)))
    distances = scipy.spatial.distance.pdist(vectorsMatrix, "jaccard")
    return distances

def createRankingsJSON(subredditVectors, distanceMatrix, topXSubs):
    print "Creating rankings JSON...\n"
    jsonDistances = {}
    completed = 0
    for subreddit in subredditVectors:
        idx = subredditVectors.keys().index(subreddit)
        row = list(distanceMatrix[idx])
        names = [sub for idx, sub in enumerate(subredditVectors.keys()) if row[idx] != 0]
        sortedNames = sorted(names, reverse = True, key = lambda x: row[subredditVectors.keys().index(x)])
        jsonDistances[subreddit] = sortedNames[0: topXSubs]
        completed += 1
        if completed % 1000 == 0:
            print "\tProcessed %s subreddits...\n" % (completed)
    with open("distanceMatrix.json", "w") as matrix:
        json.dumps(jsonDistances, matrix)
