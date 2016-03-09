from createRankings import *
from createWordClouds import *

# Create the Recommendation Engine's JSON file
print "Beginning work on creating data for Recommendation Engine.\n\n"
topSubreddits = fetchTopSubreddits(100, 10000)
print "Fetched top subreddits.\n"
users = fetchUsers()
print "Fetched users.\n"
subredditVectors = mapUserVectors(topSubreddits, users)
print "Created subreddit vectors.\n"
vectorsMatrix = createVectorsMatrix(subredditVectors)
print "Created vectors matrix.\n"
distancesMatrix = createDistanceMatrix(subredditVectors, vectorsMatrix)
print "Created distance matrix.\n"
createRankingsJSON(subredditVectors, distancesMatrix, 50)
print "Created Recommendation Engine JSON.\n\n"

# Create the Word Clouds JSON file
print "Beginning work on creating data for Word Clouds.\n\n"
createWordsJSON(50, topSubreddits.keys())
print "Created Word Cloud JSON.\n"
