import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

def plotDecadeHistogram(data, min_decade, max_decade, filename, title, xlabel, ylabel):
	# example data
	# mu = 100 # mean of distribution
	# sigma = 15 # standard deviation of distribution
	# x = mu + sigma * np.random.randn(10000)

	# num_bins = 50
	# the histogram of the data

	num_bins = (max_decade - min_decade) / 10 + 1
	print num_bins

	n, bins, patches = plt.hist(data, num_bins, range=(min_decade,max_decade), normed=True, facecolor='green', alpha=0.5)
	#n, bins, patches = plt.hist(data, num_bins, facecolor='green', alpha=0.5)

	print n
	print sum(n)
	print bins
	print patches

	# add a 'best fit' line
	# y = mlab.normpdf(bins, mu, sigma)
	# plt.plot(bins, y, 'r--')
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.title(title)

	# Tweak spacing to prevent clipping of ylabel
	plt.subplots_adjust(left=0.15)
	plt.savefig(filename)
	plt.close()

def plotProbabilityForMovieInDecadeHistogram(data, min_decade, max_decade, filename, title, xlabel, ylabel):
	# example data
	# mu = 100 # mean of distribution
	# sigma = 15 # standard deviation of distribution
	# x = mu + sigma * np.random.randn(10000)

	# num_bins = 50
	# the histogram of the data

	num_bins = (max_decade - min_decade) / 10 + 1
	print num_bins

	n, bins, patches = plt.hist(data, num_bins, range=(min_decade,max_decade), , facecolor='green', alpha=0.5)
	#n, bins, patches = plt.hist(data, num_bins, facecolor='green', alpha=0.5)

	print n
	print sum(n)
	print bins
	print patches

	# add a 'best fit' line
	# y = mlab.normpdf(bins, mu, sigma)
	# plt.plot(bins, y, 'r--')
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.title(title)

	# Tweak spacing to prevent clipping of ylabel
	plt.subplots_adjust(left=0.15)
	plt.savefig(filename)
	plt.close()


if __name__ == '__main__':

	# example data
	mu = 100 # mean of distribution
	sigma = 15 # standard deviation of distribution
	x = mu + sigma * np.random.randn(10000)

	print(len(x))

	num_bins = 50

	plotDecadeHistogram(x, num_bins, 'plot.png', 'Histogram of P(Y) across the entire dataset', 'Decade', 'Probability')