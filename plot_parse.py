import gzip
import re

import plots
import random
import string
from math import log as log

from datetime import datetime
import numpy as np
import stop_words

#def 
stopWords = {str(word):0 for word in stop_words.get_stop_words('English')}

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
        word = word.translate(None, string.punctuation).lower()
        if word in stopWords:
            continue
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
    bagOfWords = {key:{0: len(dataset)} for key in wordDictionary.iterkeys()}

    #for each movie in the dataset, vote for the number of times the word is used in the summary
    for movie in dataset:
        for word in movie['word_map']:
            #print word
            value = movie['word_map'][word]

            if value in bagOfWords[word]:
                bagOfWords[word][value] += 1
            else:
                bagOfWords[word][value] = 1

            bagOfWords[word][0] -= 1

        # for word in bagOfWords.iterkeys():

        #     #determine how many times the word is used
        #     if word in movie['word_map']:
        #         value = movie['word_map'][word]
        #     else:
        #         value = 0

        #     #vote in the decade-wide bag of words
        #     if value in bagOfWords[word]:
        #         bagOfWords[word][value] += 1
        #     else:
        #         bagOfWords[word][value] = 1

    def probabilityFunction(wi, xi):
        if wi in bagOfWords:
            if xi in bagOfWords[wi]:
                if bagOfWords[wi][xi] == 0:
                    return dirlect
                else:
                    probability = float(bagOfWords[wi][xi])/float(datasetLength)
                    #print 'computed probability: {}'.format(probability)
                    return probability
            else:
                return dirlect
        else:
            if xi == 0:
                return maxProb
            else:
                return dirlect

    return probabilityFunction

# def generateProbabilityFunctionForDataOld(dataset):


#     #get bag of words for entire data set
#     #initialize bag of words
#     # each word has a dictionary containing the number of times the word is present and the number of movies voting for it
#     wordDictionary = reduce(dictReducer, [movie['word_map'] for movie in dataset], {})
#     datasetLength = len(dataset)
#     #generate the bag of words for this decade
#     bagOfWords = {key:{} for key in wordDictionary.iterkeys()}

#     #for each movie in the dataset, vote for the number of times the word is used in the summary
#     for movie in dataset:

#         for word in bagOfWords.iterkeys():

#             #determine how many times the word is used
#             if word in movie['word_map']:
#                 value = movie['word_map'][word]
#             else:
#                 value = 0

#             #vote in the decade-wide bag of words
#             if value in bagOfWords[word]:
#                 bagOfWords[word][value] += 1
#             else:
#                 bagOfWords[word][value] = 1


#     #print bagOfWords['the']
#     #function returns #votes for #times the word shows up in the plot summary
#     #divided by the total number of entries in the dataset

#     #note that if the word didnt exist in the original bag of words we 
#     #return very high probability for xi=0, otherwise very small probability



#     def probabilityFunction(wi, xi):
#         if wi in bagOfWords:
#             if xi in bagOfWords[wi]:
#                 if bagOfWords[wi][xi] == 0:
#                     return dirlect
#                 else:
#                     probability = float(bagOfWords[wi][xi])/float(datasetLength)
#                     #print 'computed probability: {}'.format(probability)
#                     return probability
#             else:
#                 return dirlect
#         else:
#             if xi == 0:
#                 return maxProb
#             else:
#                 return dirlect

#     return probabilityFunction



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

    print 'Start time: {}'.format(datetime.now())
    all_movies = list(load_all_movies("./plot.list.gz"))
    print 'Loaded all movies time: {}'.format(datetime.now())
    # all_movies.append({"title": "dummy",
    #                              "year": 2020,
    #                              'identifier': 'identifier',
    #                              'episode': 'episode',
    #                              "summary": []})

    #print('min year = {}, max year = {}'.format(min_year, max_year))

    #first = load_all_movies("./plot.list.gz").next()
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

    def generateTrainingAndTestData(movieData):
        decades = [1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010]
        balanced_movies = []
        trainingSet = []
        testSet = []

        train_x = []
        test_x = []
        train_y = []
        test_y = []


        for decade in decades:
            decade_data = [movie for movie in movieData if movie['year']==decade]
            if(len(decade_data) < 6000):
                print 'Decade {} contains fewer than 6000 movies'.format(decade)
            decade_subset = random.sample(decade_data, 6000)
            balanced_movies.extend(decade_subset)
            balanced_movies_train = random.sample(decade_subset,4800)
            trainingSet.extend(balanced_movies_train)
            balanced_movies_test = [movie for movie in decade_subset if movie not in balanced_movies_train]
            testSet.extend(balanced_movies_test)
            train_x.append( [movie['summary'] for movie in balanced_movies_train])
            test_x.append( [movie['summary'] for movie in balanced_movies_test])
            train_y.append( [movie['year'] for movie in balanced_movies_train])
            test_y.append( [movie['year'] for movie in balanced_movies_test])

        #return (balanced_movies,)

        return (balanced_movies, trainingSet, testSet, train_x, test_x, train_y, test_y)


    ret = generateTrainingAndTestData(all_movies)
    balanced_movies = ret[0]
    #trainingSet = balanced_movies
    trainingSet = ret[1]
    print 'Training Set Len: {}'.format(len(trainingSet))
    testSet = ret[2]
    print 'Test Set Len: {}'.format(len(testSet))
    print 'Data sets generated time: {}'.format(datetime.now())

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
    decades = [1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010]
    for decade in decades:
        movies_for_decade = filter(lambda x : x["year"] == decade, trainingSet)
        probabilityFunctionForDecade[decade] = generateProbabilityFunctionForData(movies_for_decade)
    #print probabilityFunctionForDecade
    print 'Probability functions generated time: {}'.format(datetime.now())

    # probabilityFunctionForDecadeOld = {}
    # decades = [1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010]
    # for decade in decades:
    #     movies_for_decade = filter(lambda x : x["year"] == decade, trainingSet)
    #     probabilityFunctionForDecadeOld[decade] = generateProbabilityFunctionForDataOld(movies_for_decade)

    # print probabilityFunctionForDecadeOld
    # print 'Old Probability functions generated time: {}'.format(datetime.now())

    bagOfWordsList = []
    for movie in trainingSet:
        bagOfWordsList.extend(movie['word_map'].keys())

    #this is the bag of words for the balanced set of movies
    bagOfWords = set(bagOfWordsList)

    print 'Bag of words generated time: {}'.format(datetime.now())

    def createFeatureVectorFromWordMap(word_map):
        feature_vector = word_map.copy()

        #print 'Computing feature vector from word map'
        #print 'word map'
        #print word_map
        for word in bagOfWords:
            if word not in feature_vector:
                feature_vector[word] = 0

        #print 'feature vector'
        #print feature_vector
        return feature_vector

    zeroProbabilitySums = {}
    for decade in decades:

        zeroProbabilitySum = reduce(lambda sum, word: sum + log(probabilityFunctionForDecade[decade](word, 0)), bagOfWords, 0)
        zeroProbabilitySums[decade] = zeroProbabilitySum

    def computeProbabilityForDecadeAndWordMap(decade, word_map):

        #print 'creating feature vector'
        #featureVector = createFeatureVectorFromWordMap(word_map)
        zeroProbability = zeroProbabilitySums[decade]
        probabilityFunction = probabilityFunctionForDecade[decade]

        def probabilityReducer(accumulatedLogProbabilty, feature):
            #print feature
            probability = probabilityFunction(feature[0], feature[1])
            zeroProbForThisWord = probabilityFunction(feature[0], 0)
            #print probability
            return accumulatedLogProbabilty + log(probability) - log(zeroProbForThisWord)
            #return 0
        
        #probability = reduce(probabilityReducer, featureVector.iteritems(), zeroProbability)
        probability = reduce(probabilityReducer, word_map.iteritems(), zeroProbability)
        #probability = 0
        return probability



    # movie = moviesDict[moviesDict.keys()[0]]
    # decade = 1930

    # print '*****************************'
    # print 'Computing probability for {}'.format(movie['title'])
    # probability = computeProbabilityForDecadeAndWordMap(decade, movie['word_map'])
    # print '{}: {}'.format(decade, probability)


    mainPredictions = np.empty([len(decades)])
    for movie in moviesDict.itervalues():
        print '*****************************'
        print 'Computing probabilities for {}'.format(movie['title'])

        #probabilities[movie['title']] = []

        for i, decade in enumerate(decades):
            mainPredictions[i] = computeProbabilityForDecadeAndWordMap(decade, movie['word_map'])

            #print '{}: {}'.format(decade, probability)
            #probabilities[movie['title']].append(probability)

        correctDecade = movie['year']
        predictedDecade = decades[np.argmax(mainPredictions)]
        # print predictions[i]
        print 'Correct Decade: {}, Prediced Decade: {}\n'.format(correctDecade, predictedDecade)

    print 'Major Movies time: {}'.format(datetime.now())


    #create numpy (n*m, s.t. n=length of training set, m=# of decades) array
    predictions = np.empty([len(testSet), len(decades)])
    for i, movie in enumerate(testSet):
        for j, decade in enumerate(decades):
            predictions[i, j] = computeProbabilityForDecadeAndWordMap(decade, movie['word_map'])

    #2k - expected accuracy of the classifier
    correctPredictions = 0
    for i, movie in enumerate(testSet):
        correctDecade = movie['year']
        predictedDecade = decades[np.argmax(predictions[i])]
        # print predictions[i]
        # print 'Correct Decade: {}, Prediced Decade: {}'.format(correctDecade, predictedDecade)
        if correctDecade == predictedDecade:
            correctPredictions += 1

    print 'Correctly predicted {} out of {}, for an accuracy of {}'.format(correctPredictions, len(testSet), float(correctPredictions)/float(len(testSet)))

    #2l - CMC
    kData = np.zeros([len(decades)])
    for i, movie in enumerate(testSet):
        sortedIndices = list(np.argsort(predictions[i]))
        sortedIndices.reverse()
        print sortedIndices
        correctDecadeIndex = decades.index(movie['year'])
        print correctDecadeIndex
        for j in range(len(sortedIndices)):
            if correctDecadeIndex == sortedIndices[j]:
                kData[j] += 1
                break

    #print kData
    lastSum = 0
    cmcCurveData = np.empty([len(decades)])
    for i in range(len(kData)):
        cmcCurveData[i] = lastSum + kData[i]
        lastSum = cmcCurveData[i]


    print cmcCurveData/len(testSet)













    




    # => 379451