import tweepy
import json
import pandas as pd
import player as player
import game as game
#import folder.file as myModule
#k = myModule.Klasa()
# Converts the file to an array of lines
def getLines(fileName):
    with open(fileName) as f:
        lines = f.readlines()
    return lines

def printData(lines):
    for line in lines:
        print(line)
        
def parseData(line):
    parts = line.split("::")
    week9game = game.Game(parts[1], parts[2], parts[3], "placeholder")
    player1 = player.Player(parts[0], week9game)
    print(player1.name)
    print(player1.games.points)
#    for part in parts:
#        print(part)

def readTweets():
    # get all the users
    for user in tweepy.Cursor(api.search_users, q='#fantasyfootball').items(10):
        tweets = api.user_timeline(user.id)
        # get one of the users tweets
        tweet = tweets[0]
        tweetText = tweet.text.replace('\n','')
        formatted = '{}::::{}::::{}::::{}::::{}\n'.format(user.name, user.id, tweet.created_at, tweet.retweet_count, tweetText)
        outputFile.write(formatted)

def createPlayer(lineFromFile):
    player = {}
    player.Name = lineFromFile


# setup the authorization
exec(open("..\config\TwitterTokens.py").read())

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit = True)

# create output file
outputFile = open("ffb_output.txt", "w", encoding="utf-8")
outputFile.close()

#read in the stats
statsFile = open("..\config\week9.dat", "r", encoding="utf-8") 
week9data = getLines("..\config\week9.dat")

players = []
#parse the data
for line in week9data:
    parsedLine = parseData(line)
    
#printData(week9data)
