import tweepy
import player as player
import game as game
import fantasyExpert as fantasyExpert

# Converts the file to an array of lines
def getLines(fileName):
    with open(fileName) as f:
        lines = f.readlines()
    return lines

def printPlayers():
    for player1 in players:
        formatted = "{}  {}  {}\n".format(player1.name, player1.games.points, player1.numOfTweets)
        print(formatted)
        
def parseData(line):
    parts = line.split("::")
    week9game = game.Game(parts[1], parts[2], parts[3], "placeholder")

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
            if player1.name in tweet.text: # or player1.nickname in tweet.text:
#                print("{}::{} {}\n".format(player1.name, player1.nickname, tweet.text))
                player1.numOfTweets = player1.numOfTweets + 1
            elif player1.nickname != "" and player1.nickname in tweet.text:
#                print("Nickname {}::{} {}\n".format(player1.name, player1.nickname, tweet.text))
                player1.numOfTweets = player1.numOfTweets + 1

def getExpertsTweets(username):
#    for user in tweepy.Cursor(api.search_users, q='villanova').items(50):
#    ffbUser = api.get_user(username)
    sinceId = 1059166842206355456 # tweet on nov 4 at 11:33am
    maxId = 1060954187406565376 # tweet on nov 9 at 9:56am
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