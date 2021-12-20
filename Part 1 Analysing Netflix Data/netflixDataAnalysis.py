# code by @jolenechong on github
import requests  #for api
import pandas as pd
from collections import Counter #for api part

# read the csv file
df = pd.read_csv('Part 1 Analysing Netflix Data/SampleViewingAcitivty.csv')

# print(list(df.columns))

# get only my data
# only return rows with ur name in profile name column
# df = df[df["Profile Name"].str.contains("Jolene")]

# longest session
# basically i wna see what movie i watch in one sitting and how long that one sitting was
def longestSession():
    print('Longest Session:',df["Duration"].max())
    longsess = df["Duration"].max()
    # find index of longest duration according to excel sheet
    longsess_idx = df.index[df["Duration"] == longsess][0] #get first match of longest duration index
    # get entire row using the index    
    longsess = df.iloc[[longsess_idx]] #takes in a list and returns all the data in that row
    print("You watched", longsess["Title"].values[0], "for", longsess["Duration"].values[0])
# longestSession()

# drop the unecessary columns
df = df.drop(["Profile Name", 'Attributes', 'Supplemental Video Type',
             'Device Type', 'Bookmark', 'Latest Bookmark', 'Country'], axis=1)
# print(df.head())

# correct format of date and times
# dun copy this first show wat happens if dh this
df['Duration'] = pd.to_timedelta(df['Duration'])
df['Start Time'] = pd.to_datetime(df['Start Time'])

def totalNetflix():
    totalDuration = df["Duration"]
    print(totalDuration.shape)
    # only return rows if its more than a minute
    totalDuration = totalDuration[(totalDuration > '0 days 00:01:00')]
    print(totalDuration.shape)
    print("total time spent on netflix:", totalDuration.sum())

# totalNetflix()

def totalTimeSpent(movie):
    moviename = df[df['Title'].str.contains(movie, regex=False)]
    print("time spend watching",movie,moviename["Duration"].sum())

# totalTimeSpent('Shutter Island')
# totalTimeSpent('The Chase')
# totalTimeSpent('Strangers From Hell')

# when we watch netflix
# which day we watch netflix most often
# if uw which day u watch the most u need to use duration
from matplotlib import pyplot as plt

def whenWatch():
    pd.options.mode.chained_assignment = None  # default='warn' use this to remove warnings

    df['weekday'] = df['Start Time'].dt.weekday #returns 0 to 6
    df['hour'] = df['Start Time'].dt.hour # return the hour of the day from 0 23

    # print(df['hour'])

    # set categories -> days
    df['weekday'] = pd.Categorical(df['weekday'], categories=[0,1,2,3,4,5,6], ordered=True)

    watchByDay = df['weekday'].value_counts() #count how many mondays, tuesdays etc
    # make monday first, ordered by date to fit in categories
    # print(watchByDay)
    # make monday first, ordered by date to fit in categories
    watchByDay = watchByDay.sort_index() #now is according to what the rows is in the excel but we sort by mon tues wed now
    watchByDay.plot(kind='bar', figsize=(20,10),title='Netflix Shows Watched By Day')
    plt.show()

whenWatch()

# CHALLENGE: try to use duration instead of counts

'''
API
'''
def findGenre(title):
    API_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' #use your own API key
    url = "https://imdb8.p.rapidapi.com/title/find"

    querystring = {"q":title}

    headers = {
        'x-rapidapi-host': "imdb8.p.rapidapi.com",
        'x-rapidapi-key': API_KEY
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    movieCode = response.json()
    # might not be accurate cuz we only care abt the first response
    try:
        movieCode = movieCode['results'][0]['id']
        movieCode = movieCode[7:]
        # print(movieCode)

        url = "https://imdb8.p.rapidapi.com/title/get-overview-details"

        querystring = {"tconst":movieCode,"currentCountry":"US"}

        headers = {
            'x-rapidapi-host': "imdb8.p.rapidapi.com",
            'x-rapidapi-key': API_KEY
            }

        response = requests.request("GET", url, headers=headers, params=querystring)

        response = response.json()
        movieGenres = response['genres']
        return movieGenres
        # print(movieGenres)
    except:
        return 'no data found'

# findGenre('Trailer') #this will return no data found cuz their API dun hv this record
# print(findGenre('Strangers from hell'))

def findGenres():
    movies = list(df['Title'])
    genres = []
    no_duplicate_movielist = []

    for movie in movies:
        # print(movie.find(':'))
        if movie.find(':') != -1: #movie.find returns -1 if it doesn't find anyth
            movie = movie[:movie.find(':')]
            # print(movie)

        if movie.find('_') != -1:
            movie = movie[:movie.find('_')]

        no_duplicate_movielist.append(movie)

    no_duplicate_movielist = list(dict.fromkeys(no_duplicate_movielist))

    print(no_duplicate_movielist)

    for movie in no_duplicate_movielist:
        genres.append(findGenre(movie))
    
    print(genres)

# fill in list according to the output from the function above, js copy paste
genres = [['Drama', 'Family', 'Sci-Fi'], ['Adventure', 'Drama', 'Horror', 'Thriller'], ['Adventure', 'Drama', 'Horror', 'Thriller'], ['Crime', 'Drama', 'Mystery', 'Thriller'], ['Comedy', 'Romance'], ['Action', 'Drama', 'Mystery', 'Thriller'], 'no data found', ['Drama', 'Mystery'], ['Crime', 'Horror', 'Mystery'], ['Drama', 'Horror', 'Mystery', 'Thriller'], ['Action', 'Drama', 'Horror', 'Sci-Fi'], ['Comedy', 'Drama', 'Music', 'Romance'], ['Mystery', 'Thriller'], ['Action', 'Adventure', 'Thriller'], ['Action', 'Crime', 'Drama', 'Sci-Fi', 'Thriller'], ['Crime', 'Drama', 'Thriller'], ['Action', 'Crime', 'Thriller'], ['Horror', 'Mystery'], 'no data found', ['Action', 'Adventure', 'Drama', 'Fantasy', 'Sci-Fi'], ['Horror', 'Mystery', 'Thriller'], ['Action', 'Drama', 'Horror', 'Thriller'], 'no data found', ['Drama', 'Romance'], ['Action', 'Horror', 'Thriller'], ['Comedy', 'Horror'], ['Drama', 'Romance'], ['Drama', 'History', 'Romance'], ['Crime', 'Mystery', 'News'], ['Comedy'], ['Comedy', 'Drama'], ['Comedy', 'Drama', 'Romance'], ['Action', 'Adventure', 'Mystery', 'Sci-Fi'], ['Drama', 'Horror', 'Mystery'], ['Drama', 'Thriller'], ['Adventure', 'Drama', 'Fantasy', 'Romance'], ['Drama', 'Fantasy', 'Romance'], ['Mystery', 'Thriller'], ['Biography', 'Crime', 'Drama', 'History', 'Mystery', 'Thriller'], ['Horror', 'Thriller'], ['Game-Show', 'Reality-TV'], ['Crime', 'Drama', 'Thriller'], ['Comedy'], ['Comedy', 'Romance'], ['Action', 'Comedy', 'Romance'], ['Crime', 'Drama', 'Mystery', 'Thriller'], ['Action', 'Comedy', 'Crime', 'Thriller'], ['Fantasy', 'Horror', 'Thriller'], ['Horror', 'Mystery', 'Thriller'], ['Drama', 'Horror', 'Thriller'], ['Horror', 'Mystery', 'Thriller'], ['Drama', 'Horror', 'Mystery', 'Thriller'], ['Horror', 'Mystery', 'Thriller'], ['Horror', 'Thriller'], ['Drama', 'Horror', 'Thriller'], ['Drama'], ['Action', 'Comedy', 'Fantasy'], ['Horror', 'Mystery', 'Thriller'], ['Crime', 'Drama', 'Thriller'], ['Comedy', 'Family'], ['Mystery', 'Thriller'], ['Action', 'Adventure', 'Crime', 'Drama', 'Thriller'], ['Drama', 'Horror', 'Mystery', 'Thriller'], ['Horror', 'Thriller'], ['Crime', 'Horror', 'Thriller'], ['Crime', 'Drama', 'Thriller'], ['Horror', 'Sci-Fi', 'Thriller'], ['Action', 'Crime', 'Drama', 'Mystery', 'Thriller']]

def flatten(listoflists):
    rt = []
    for i in listoflists:
        if isinstance(i,list):
            # if i is an instance of the list (checking if its a value or another list)
            # if its another list den flatten
            rt.extend(flatten(i)) #goes back up and adds it to the final list aft the end of the call tree
        else: 
            # else append
            rt.append(i)
    return rt

def favouriteGenres(genres):
    genreList = flatten(genres)

    c = Counter(genreList)
    print (c.most_common(3))

favouriteGenres(genres)