import matplotlib
import glob
import numpy
import pandas
from sklearn import cluster
from sklearn import decomposition
from sklearn import neighbors
from matplotlib import pyplot
from PIL import Image


def primary_colours(x):
    km = cluster.MiniBatchKMeans(5)
    km.fit(x)
    return km.cluster_centers_

