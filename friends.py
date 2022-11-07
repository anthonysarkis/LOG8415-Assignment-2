from operator import add

from pyspark.sql import SparkSession

def processInput(line):
    """
    processInput processes a line of the input text file to get the userId and a list of his friends, all as integers
    :param string line:     A line of the text file format as: "userid\tfriend1,friend2..."
    :return:                A tuple of the userid and a list of his friends (key: userId, value: [friend1, friend2, ...])
    """
    splittedLine = line.split('\t')
    userId = int(splittedLine[0])
    if(len(splittedLine) == 1):
        return (userId, [])
    
    friendsStr = splittedLine[1]
    if(len(friendsStr) == 0):
        return (userId, [])
    friends = friendsStr.split(',')
    friendIds = [int(friend) for friend in friends]
    return (userId, friendIds)

def getPairsOfFriends(line):
    """
    getPairOfFriends takes a user and his friends and returns a list of all pairs of friends with the type: "m" for mutual and "d" for direct friends
    : param line:       A tuple of a user and his direct friends (key: userId, value: [friend1, friend2, ...])
    :return:            A list of tuples [(key: (user1, user2), value: "m" or "d")]
    """
    if(len(line) < 2):
        return []
    user, friends = line
    
    mutualFriends = []
    for i in range(0, len(friends)-1):
        for j in range(i+1, len(friends)):
            mutualFriends.append(((friends[i], friends[j]), ["m"]))
            mutualFriends.append(((friends[j], friends[i]), ["m"]))
    
    directFriends = []
    for friend in friends:
        directFriends.append(((user, friend), ["d"]))
    directFriends.append(((user, user), ["d"]))

    return directFriends + mutualFriends

def getTopFriendRecommendations(line):
    """
    getTopFriendRecommendations returns the 10 friends to recommend for a user
    :param line:        A list of all the users that have mutual friends with the user and the number of mutual friends (key: friend, value: nMutualFriends)
    :return:            A list of the ids of the 10 friends that have the most mutual friends with user, sorted
    """
    friendsAndConnections = list(line)
    sortedList = sorted(friendsAndConnections, key=lambda element: (element[1], -element[0]), reverse=True)
    topTenRecommendations = []
    for index, element in enumerate(sortedList[0:10]):
        topTenRecommendations.append(element[0])
        if index==10:
            break
    return topTenRecommendations

def formatLine(line):
    """
    formatLine formats the data to output as <USERID><TAB><RECOMMENDATIONS>
    :param line:        A tuple of the userId and a list of the users to recommend
    :return:            Formatted data
    """
    userId, usersToRecommend = line[0], line[1]
    return str(userId) + "\t" + ",".join([str(x) for x in usersToRecommend])

if __name__ == "__main__":
    input = "friends_input.txt"

    spark = SparkSession\
        .builder\
        .appName("PythonFriendsRecommend")\
        .getOrCreate()

    def userToFriendsAndConnections(line):
        """
        userToFriendsAndConnections is used to get a user and a user he has mutual friends with with the number of mutual friends. 
                                    removes the line if user1 and user2 are direct friends
        :param line:        (key: (user1, user2), value: number of mutual friends between user1 and user2)
        :return:            A list of tuples (key: user1, value: [(user2, number of mutual friends)])
        """
        if "d" not in line[1]:
            user1 = line[0][0]
            user2 = line[0][1]
            nMutualFriends = len(line[1])
            return [(user1, [(user2, nMutualFriends)])]
        return []

    # solution
    # Processed version of the text file (key: userId, value: list of user's direct friends)
    userToFriends = spark.read.text(input).rdd.map(lambda lineData: processInput(lineData[0]))
    # (key: userId, value: sorted list of top ten users that aren't direct friend with userId and that have the most mutual friends with userId)
    userToRecommendations = userToFriends\
         .flatMap(lambda line: getPairsOfFriends(line)).reduceByKey(add)\
             .flatMap(lambda line: userToFriendsAndConnections(line)).reduceByKey(add)\
                      .mapValues(lambda line: getTopFriendRecommendations(line))
    # (key: userId of users that have nobody to be recommended aka. have no friends, or only friends that have no friends, value: empty list)
    usersWithEmptyRecommendations = userToFriends.subtractByKey(userToRecommendations).mapValues(lambda l: [])
    # (key: userId of all users, value: list of recommendations)
    allUsersRecommendations = userToRecommendations.union(usersWithEmptyRecommendations).map(lambda line: formatLine(line))
    
    allUsersRecommendations.saveAsTextFile("friends_output")

    spark.stop()
