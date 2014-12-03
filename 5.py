from datetime import datetime
from sklearn import svm
from sklearn.feature_selection import SelectKBest
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import RandomizedPCA,TruncatedSVD
from sklearn.random_projection import GaussianRandomProjection
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import f_regression
from sklearn.pipeline import Pipeline
from sklearn import linear_model, svm, neighbors
import numpy as np
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

def get_prediciton_accuracy(train_x,train_y,test_x,test_y,classifier_name):
    classifiers = {
        'SGD': linear_model.SGDClassifier(),
        'SVC Linear': svm.LinearSVC(),
        'SVC rbf': svm.SVC(kernel='rbf'),
        'L1 Perceptron': linear_model.Perceptron(penalty='l1'),
        'L2 Perceptron': linear_model.Perceptron(penalty='l2', n_iter=25),
        'NN': neighbors.NearestNeighbors(),
    }
    clf = Pipeline([('vector', CountVectorizer(encoding='latin-1')),\
                    #('SVD', TruncatedSVD(n_components=150)),
                    ('GRP', GaussianRandomProjection(n_components=10000)),\
                    ('Scaler', StandardScaler()),\
                    (classifier_name,classifiers[classifier_name])])
    clf = clf.fit(train_x,train_y)
    predicted = clf.predict(test_x)
    return np.mean(predicted == test_y)

if __name__ == '__main__':
    print datetime.now().time()
    all_movies = list(load_all_movies("./plot.list.gz"))

    first = load_all_movies("./plot.list.gz").next()
    #generate balanced dataset
    decades = [1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010]
    balanced_movies = []
    train_x = []
    train_y = []
    test_x=[]
    test_y=[]
    for decade in decades:
        decade_data = [movie for movie in all_movies if movie['year']==decade]
        if(len(decade_data) < 6000):
            print 'Decade {} contains fewer than 6000 movies'.format(decade)
        decade_subset = random.sample(decade_data, 6000)
        balanced_movies.extend(decade_subset)
        balanced_movies_train = random.sample(decade_subset,3000)
        balanced_movies_test = [movie for movie in decade_subset if movie not in balanced_movies_train]
        train_x = train_x +  [movie['summary'] for movie in balanced_movies_train]
        test_x = test_x + [movie['summary'] for movie in balanced_movies_test]
        train_y = train_y +  [movie['year'] for movie in balanced_movies_train]
        test_y = test_y + [movie['year'] for movie in balanced_movies_test]

    print datetime.now().time()
    print "classifying function"
    classifiers = ['SGD','SVC Linear','SVC rbf','L1 Perceptron','L2 Perceptron','NN']
    for classifier_name in classifiers:
        print classifier_name
        print get_prediciton_accuracy(train_x,train_y,test_x,test_y,classifier_name)
        print datetime.now().time()