import tweepy
import player as player
import game as game
import fantasyExpert as fantasyExpert
import matplotlib.pyplot as plt
from operator import attrgetter

def createPlot(players):
        
    sortedList = sorted(players, key=attrgetter('games.points'))
    x = []
    y = []
#    print('\n\nafter sorting list')
    for player1 in sortedList:
#        print('{} {} {}'.format(player1.name, player1.games.points, player1.games.numOfTweets))
        x.append(player1.games.points)
        y.append(player1.games.numOfTweets)
    
    colors = (0,0,0)
     
    # Plot
    plt.scatter(x, y, s=15, c=colors, alpha=0.5)
    plt.title('Fantasy Football points vs # of Tweets')
    plt.xlabel('# of Points')
    plt.ylabel('# of Tweets')
    plt.show()
    
# Converts the file to an array of lines
def getLines(fileName):
    with open(fileName) as f:
        lines = f.readlines()
    return lines

def printPlayers():
    for player1 in players:
        formatted = "{}  {}  {}".format(player1.name, player1.games.points, player1.games.numOfTweets)
        print(formatted)
        
def parseData(line):
    parts = line.split("::")
    week9game = game.Game(float(parts[1]), parts[2], parts[3])

    player1 = player.Player(parts[0], parts[4], week9game)        
    
    return player1

def readTweets(player1):
    for tweet in tweepy.Cursor(api.search, q=player1.name).items(10):
        tweetText = tweet.text.replace('\n','')
        formatted = '{}::::{}::::{}::::{}\n'.format(tweet.created_at, tweet.retweet_count, tweetText, tweet.id)
        outputFile.write(formatted)
        
def associateTweetsWithPlayer(tweets):
    for player1 in players:
        for tweet in tweets:
            if player1.name in tweet.text:
                player1.games.numOfTweets = player1.games.numOfTweets + 1
            elif player1.nickname != "" and player1.nickname in tweet.text:
                player1.games.numOfTweets = player1.games.numOfTweets + 1

def getExpertsTweets(username):
    sinceId = 1059166842206355456 # tweet on nov 4 at 11:33am
    maxId = 1059809473622171649 # tweet on nov 6 at 6:07am
            
    tweets = []
    try:
        tweets = api.user_timeline(username, since_id=sinceId, max_id=maxId, count=200)
        # get one of the users tweets
        if tweets:
            for tweet in tweets:
                tweetText = tweet.text.replace('\n','')
                formatted = "{} {} {}\n".format(username, tweetText, tweet.created_at)
                outputFile.write(formatted)
                
    except:
        print("Username {} was not found".format(username))
        
    return tweets

players = []
experts = []

# setup the authorization
exec(open("..\config\TwitterTokens.py").read())

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit = True)

# create output file
outputFile = open("..\output\week9_tweets.txt", "w", encoding="utf-8")

# read in the stats
week9data = getLines("..\config\week9.dat")

# get the list of fantasy football experts
ffbExperts = getLines(r"..\config\users.dat")

# parse the data
for line in week9data:
    player1 = parseData(line)
    players.append(player1)
#    readTweets(player1)

for expert in ffbExperts:
    tweets = getExpertsTweets(expert)
    expert1 = fantasyExpert.FantasyExpert(expert, tweets)
    associateTweetsWithPlayer(tweets)
    experts.append(expert1)

    
outputFile.close()

printPlayers()

createPlot(players)