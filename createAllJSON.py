from createRankings import *
from createWordClouds import *

# Create the Recommendation Engine's JSON file
topSubreddits = fetchTopSubreddits(100, 10000)
users = fetchUsers()
subredditVectors = mapUserVectors(topSubreddits, users)
vectorsMatrix = createVectorsMatrix(subredditVectors)
distancesMatrix = createDistanceMatrix(subredditVectors, vectorsMatrix)
createRankingsJSON(subredditVectors, distancesMatrix, 50)

# Create the Word Clouds JSON file
createWordsJSON(50, topSubreddits.keys())
