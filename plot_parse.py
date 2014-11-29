import gzip
import re

import plots
import random
import string
from math import log as log

#def 


moviesDict = {}
def load_all_movies(filename):
    """
    Load and parse 'plot.list.gz'. Yields each consecutive movie as a dictionary:
        {"title": "The movie's title",
         "year": The decade of the movie, like 1950 or 1980,
         "identifier": Full key of IMDB's text string,
         "summary": "The movie's plot summary"
        }
    You can download `plot.list.gz` from http://www.imdb.com/interfaces
    """
    assert "plot.list.gz" in filename # Or whatever you called it
    current_movie = None
    movie_regexp = re.compile("MV: ((.*?) \(([0-9]+).*\)(.*))")

    titlesToMatch = ['Finding Nemo', 'The Matrix', 'Gone with the Wind', 'Harry Potter and the Goblet of Fire', 'Avatar']
    title_regexps = [re.compile('{}$'.format(title)) for title in titlesToMatch]


    skipped = 0
    for i,line in enumerate(gzip.open(filename)):
        if line.startswith("MV"):
            if current_movie:
                # Fix up description and send it on
                current_movie['summary'] = "\n".join(current_movie['summary'] )
                yield current_movie
            current_movie = None
            try:
                identifier, title, year, episode = movie_regexp.match(line).groups()
                if int(year) < 1930 or int(year) > 2014:
                    # Something went wrong here
                    raise ValueError(identifier)
                current_movie = {"title": title,
                                 "year": 10*int(int(year)/10),
                                 'identifier': identifier,
                                 'episode': episode,
                                 "summary": [],
                                 'word_map': {}}

                for j,regexp in enumerate(title_regexps):
                    if regexp.match(title):
                        #print 'matched {}'.format(titlesToMatch[j])
                        moviesDict[titlesToMatch[j]] = current_movie


                

                # if i%10000 == 0:
                #     print title

            except:
                skipped += 1
                # print 'Line {} was skipped'.format(i)
        if line.startswith("PL: ") and current_movie:
            # Add to the current movie's description
            summaryLine = line.replace("PL: ","")
            current_movie['summary'].append(summaryLine)
            current_movie['word_map'] = dictReducer(current_movie['word_map'], lineReducer(summaryLine))


    print "Skipped",skipped
 
def lineReducer(line):
    lineDict = {}
    for word in line.split():
        word = word.lower()
        if word in lineDict:
            lineDict[word] += 1
        else:
            lineDict[word] = 1
    return lineDict



def dictReducer(mainDict, nextDict):
    #print nextDict
    for key, value in nextDict.iteritems():
        if key in mainDict:
            mainDict[key] += value
        else:
            mainDict[key] = value
    return mainDict

dirlect = .000001
maxProb = .999999

def generateProbabilityFunctionForData(dataset):


    #get bag of words for entire data set
    #initialize bag of words
    # each word has a dictionary containing the number of times the word is present and the number of movies voting for it
    wordDictionary = reduce(dictReducer, [movie['word_map'] for movie in dataset], {})
    datasetLength = len(dataset)
    #generate the bag of words for this decade
    bagOfWords = {key:{} for key in wordDictionary.iterkeys()}

    #for each movie in the dataset, vote for the number of times the word is used in the summary
    for movie in dataset:
        for word in bagOfWords.iterkeys():

            #determine how many times the word is used
            if word in movie['word_map']:
                value = movie['word_map'][word]
            else:
                value = 0

            #vote in the decade-wide bag of words
            if value in bagOfWords[word]:
                bagOfWords[word][value] += 1
            else:
                bagOfWords[word][value] = 1

    #print bagOfWords['the']
    #function returns #votes for #times the word shows up in the plot summary
    #divided by the total number of entries in the dataset

    #note that if the word didnt exist in the original bag of words we 
    #return very high probability for xi=0, otherwise very small probability

    def probabilityFunction(wi, xi):
        if wi in bagOfWords:
            if xi in wi:
                return wi[xi]/datasetLength
            else:
                return dirlect
        else:
            if xi == 0:
                return maxProb
            else:
                return dirlect

    return probabilityFunction



    # #have movies vote

    # def probabilityFunction(wi, xi):

    #     def probabilityFunctionFilter(movie):

    #         if xi==0:
    #             if wi in movie['word_map']:
    #                 return False
    #             else:
    #                 return True

    #         else:

    #             if wi in movie['word_map']:
    #                 if movie['word_map'][wi] == xi:
    #                     return True
    #             else:
    #                 return False

    #     filteredDataSet = filter(probabilityFunctionFilter, dataset)

    #     if len(filteredDataSet) == 0:
    #         return .00000000001
    #     else:
    #         return len(filteredDataSet) / len(dataset)

    # return probabilityFunction



# def generateProbabilityFunctionForData(dataset):

#     def probabilityFunction(wi, xi):

#         def probabilityFunctionFilter(movie):

#             if xi==0:
#                 if wi in movie['word_map']:
#                     return False
#                 else:
#                     return True

#             else:

#                 if wi in movie['word_map']:
#                     if movie['word_map'][wi] == xi:
#                         return True
#                 else:
#                     return False

#         filteredDataSet = filter(probabilityFunctionFilter, dataset)

#         if len(filteredDataSet) == 0:
#             return .00000000001
#         else:
#             return len(filteredDataSet) / len(dataset)

#     return probabilityFunction

# def reducer(lineMap):
#     lineDict = {}
#     for (key, val) in lineMap:
#         if 

if __name__ == '__main__':
    all_movies = list(load_all_movies("./plot.list.gz"))
    # all_movies.append({"title": "dummy",
    #                              "year": 2020,
    #                              'identifier': 'identifier',
    #                              'episode': 'episode',
    #                              "summary": []})

    #print('min year = {}, max year = {}'.format(min_year, max_year))

    first = load_all_movies("./plot.list.gz").next()
    #print first['summary']

    # lineDictList = []
    # for line in first['summary'].split('\n'):
    #     #print line
        
    #     lineDict = lineReducer(line)
    #     #print(lineDict)

    #     lineDictList.append(lineDict)

    # lineDictList = [lineReducer(line) for line in first['summary'].split('\n')]
    # word_map = reduce(dictReducer, lineDictList, {})
    # print first['summary']
    # print first['word_map']



        #lineMapDict = map(lambda x : )



    #print first['word_map']
 
    # print(len(all_movies))
    # print(all_movies[0])

    #print all_movies[0]['word_map']

    # #2A
    # plots.plotDecadeHistogram([x["year"] for x in all_movies], 1930, 2010, 'plot2A.png', 'Histogram of P(Y) across the entire dataset', 'Decade', 'Probability')
    
    # #2B
    # plots.plotDecadeHistogram([x["year"] for x in filter(lambda x: 'radio' in x['word_map'], all_movies)], 1930, 2010, 'plot2B.png', 'Histogram of P(Y|Xradio > 0)', 'Decade', 'Probability')

    # #2C
    # plots.plotDecadeHistogram([x["year"] for x in filter(lambda x: 'beaver' in x['word_map'], all_movies)], 1930, 2010, 'plot2C.png', 'Histogram of P(Y|Xbeaver > 0)', 'Decade', 'Probability')

    # #2D
    # plots.plotDecadeHistogram([x["year"] for x in filter(lambda x: 'the' in x['word_map'], all_movies)], 1930, 2010, 'plot2D.png', 'Histogram of P(Y|Xthe > 0)', 'Decade', 'Probability')

    #generate balanced dataset
    decades = [1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010]
    balanced_movies = []
    for decade in decades:
        decade_data = [movie for movie in all_movies if movie['year']==decade]
        if(len(decade_data) < 6000):
            print 'Decade {} contains fewer than 6000 movies'.format(decade)
        decade_subset = random.sample(decade_data, 6000)
        balanced_movies.extend(decade_subset)

    # print 'The balanced data contains {} movies'.format(len(balanced_movies)) 
    
    # #2E
    # plots.plotDecadeHistogram([x["year"] for x in filter(lambda x: 'radio' in x['word_map'], balanced_movies)], 1930, 2010, 'plot2E.png', 'Histogram of P(Y|Xradio > 0) (Balanced Movies)', 'Decade', 'Probability')

    # #2F
    # plots.plotDecadeHistogram([x["year"] for x in filter(lambda x: 'beaver' in x['word_map'], balanced_movies)], 1930, 2010, 'plot2F.png', 'Histogram of P(Y|Xbeaver > 0) (Balanced Movies)', 'Decade', 'Probability')

    # #2G
    # plots.plotDecadeHistogram([x["year"] for x in filter(lambda x: 'the' in x['word_map'], balanced_movies)], 1930, 2010, 'plot2G.png', 'Histogram of P(Y|Xthe > 0) (Balanced Movies)', 'Decade', 'Probability')

    #print moviesDict

    #returns f(wi, xi)
    probabilityFunctionForDecade = {}
    for decade in decades:
        movies_for_decade = filter(lambda x : x["year"] == decade, balanced_movies)
        probabilityFunctionForDecade[decade] = generateProbabilityFunctionForData(movies_for_decade)


    bagOfWordsList = []
    for movie in balanced_movies:
        bagOfWordsList.extend(movie['word_map'].keys())

    #this is the bag of words for the balanced set of movies
    bagOfWords = set(bagOfWordsList)

    def createFeatureVectorFromWordMap(word_map):
        feature_vector = word_map.copy()

        print 'Computing feature vector from word map'
        print 'word map'
        print word_map
        for word in bagOfWords:
            if word not in feature_vector:
                feature_vector[word] = 0

        print 'feature vector'
        print feature_vector
        return feature_vector


    def computeProbabilityForDecadeAndWordMap(decade, word_map):

        featureVector = createFeatureVectorFromWordMap(word_map)
        probabilityFunction = probabilityFunctionForDecade[decade]

        def probabilityReducer(accumulatedLogProbabilty, feature):
            #print feature
            #return accumulatedLogProbabilty + log()
            return 0
        
        #probability = reduce(probabilityReducer, featureVector.iteritems, 0)
        probability = 0
        return probability



    movie = moviesDict[moviesDict.keys()[0]]
    decade = 1930

    print '*****************************'
    print 'Computing probability for {}'.format(movie['title'])
    probability = computeProbabilityForDecadeAndWordMap(decade, movie['word_map'])
    print '{}: {}'.format(decade, probability)



    # for movie in moviesDict.itervalues():
    #     print '*****************************'
    #     print 'Computing probabilities for {}'.format(movie['title'])

    #     for decade in decades:
    #         probability = computeProbabilityForDecadeAndWordMap(decade, movie['word_map'])
    #         print '{}: {}'.format(decade, probability)





    




    # => 379451