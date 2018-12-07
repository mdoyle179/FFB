from operator import attrgetter
import matplotlib.pyplot as plt

# Represents a football player
class Player:
    def __init__(self, name, nickname, games):
        self.name = name
        self.games = games
        self.nickname = nickname

    def printPlayers(players):
        tableTitle = "{:^20}  {:^20}  {:^10}".format("Player Name", "Points", "Tweets")
        print(tableTitle)
    
        sortedList = sorted(players, key=attrgetter('games.points'))
        for player1 in sortedList:
            formatted = "{:^20}  {:^20}  {:^10}".format(player1.name, player1.games.points, player1.games.numOfTweets)
            print(formatted)
            
    # Creates a scatterplot
    def createPlot(players):
        sortedList = sorted(players, key=attrgetter('games.points'))
        x = []
        y = []
        for player1 in sortedList:
            x.append(player1.games.points)
            y.append(player1.games.numOfTweets)
        
        colors = (0,0,0)
         
        # Plot
        plt.scatter(x, y, s=15, c=colors, alpha=0.5)
        plt.title('Fantasy Football points vs # of Tweets')
        plt.xlabel('# of Points')
        plt.ylabel('# of Tweets')
        plt.show()