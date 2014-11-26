import gzip
import re

import plots

#def 



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
    wordDictionary = reduce(dictReducer, lineDictList, {})
    datasetLength = len(dataset)
    bagOfWords = {key:{} for key in wordDictionary.iterkeys()}
    for movie in dataset:
        for word in bagOfWords.iterkeys():
            if word in movie['word_map']:
                value = movie['word_map'][word]
            else:
                value = 0

            if value in bagOfWords[word]:
                bagOfWords[word][value] += 1
            else
                bagOfWords[word][value] = 1


    #function returns #votes for #times the word shows up in the plot summary
    #divided by the total number of entries in the dataset

    #note that if the word didnt exist in the original bag of words we 
    #return a probability of 1 for xi=0, otherwise very small probability

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
    print first['summary']

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



    print first['word_map']
 
    # print(len(all_movies))
    # print(all_movies[0])

    #print all_movies[0]['word_map']

    #2A
    plots.plotDecadeHistogram([x["year"] for x in all_movies], 1930, 2010, 'plot2A.png', 'Histogram of P(Y) across the entire dataset', 'Decade', 'Probability')
    
    #2B
    plots.plotDecadeHistogram([x["year"] for x in filter(lambda x: 'radio' in x['word_map'], all_movies)], 1930, 2010, 'plot2A.png', 'Histogram of P(Y|Xradio > 0)', 'Decade', 'Probability')

    #2C
    plots.plotDecadeHistogram([x["year"] for x in filter(lambda x: 'beaver' in x['word_map'], all_movies)], 1930, 2010, 'plot2A.png', 'Histogram of P(Y|Xbeaver > 0)', 'Decade', 'Probability')

    # for movie in moviesOf60s:
    # decadeWordBag = reduce(dictReducer, lineDictList, {})

    #returns f(wi, xi)
    decades = {1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010}
    probabilityFunctionForDecade = {}
    for decade in decades:
        dataForDecade = filter(lambda x : x["year"] == decade, all_movies)
        probabilityFunctionForDecade[decade] = generateProbabilityFunctionForData(dataForDecade)




    # => 379451