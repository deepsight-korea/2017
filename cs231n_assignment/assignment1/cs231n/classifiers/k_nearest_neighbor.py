# -*- coding: utf8 -*-
import numpy as np
from collections import Counter

class KNearestNeighbor(object):
  """ a kNN classifier with L2 distance """

  def __init__(self):
    pass

  def train(self, X, y):
    """
    Train the classifier. For k-nearest neighbors this is just
    memorizing the training data.

    Inputs:
    - X: A numpy array of shape (num_train, D) containing the training data
      consisting of num_train samples each of dimension D.
    - y: A numpy array of shape (N,) containing the training labels, where
         y[i] is the label for X[i].
    """
    self.X_train = X
    self.y_train = y

  def predict(self, X, k=1, num_loops=0):
    """
    Predict labels for test data using this classifier.

    Inputs:
    - X: A numpy array of shape (num_test, D) containing test data consisting
         of num_test samples each of dimension D.
    - k: The number of nearest neighbors that vote for the predicted labels.
    - num_loops: Determines which implementation to use to compute distances
      between training points and testing points.

    Returns:
    - y: A numpy array of shape (num_test,) containing predicted labels for the
      test data, where y[i] is the predicted label for the test point X[i].
    """
    if num_loops == 0:
      dists = self.compute_distances_no_loops(X)
    elif num_loops == 1:
      dists = self.compute_distances_one_loop(X)
    elif num_loops == 2:
      dists = self.compute_distances_two_loops(X)
    else:
      raise ValueError('Invalid value %d for num_loops' % num_loops)

    return self.predict_labels(dists, k=k)

  def compute_distances_two_loops(self, X):
    """
    Compute the distance between each test point in X and each training point
    in self.X_train using a nested loop over both the training data and the
    test data.

    Inputs:
    - X: A numpy array of shape (num_test, D) containing test data.

    Returns:
    - dists: A numpy array of shape (num_test, num_train) where dists[i, j]
      is the Euclidean distance between the ith test point and the jth training
      point.
    """
    num_test = X.shape[0] # 500
    num_train = self.X_train.shape[0] # 5,000
    dists = np.zeros((num_test, num_train)) # (500, 5000)
    for i in xrange(num_test): # loops 500 times
      for j in xrange(num_train): # loops 5000 times
        #####################################################################
        # TODO:                                                             #
        # Compute the l2 distance between the ith test point and the jth    #
        # training point, and store the result in dists[i, j]. You should   #
        # not use a loop over dimension.                                    #
        #####################################################################
	#dists[i,j] = np.sqrt( np.sum((X[i] - self.X_train[j])**2) )
	dists[i,j] = np.linalg.norm(X[i] - self.X_train[j])
	# pass
        #####################################################################
        #                       END OF YOUR CODE                            #
        #####################################################################
    return dists

  def compute_distances_one_loop(self, X):
    """
    Compute the distance between each test point in X and each training point
    in self.X_train using a single loop over the test data.

    Input / Output: Same as compute_distances_two_loops
    """
    num_test = X.shape[0] # 500
    num_train = self.X_train.shape[0] # 5,000
    dists = np.zeros((num_test, num_train)) # (500, 5000)
    for i in xrange(num_test): # loops 500 times
      #######################################################################
      # TODO:                                                               #
      # Compute the l2 distance between the ith test point and all training #
      # points, and store the result in dists[i, :].                        #
      #######################################################################
      dists[i,:] = np.linalg.norm(self.X_train - X[i,:], axis=1)
      # Broadcasting 발생하여 (5000,3072) - (1,3072) 를 수행
      #######################################################################
      #                         END OF YOUR CODE                            #
      #######################################################################
    return dists

  def compute_distances_no_loops(self, X):
    """
    Compute the distance between each test point in X and each training point
    in self.X_train using no explicit loops.

    Input / Output: Same as compute_distances_two_loops
    """
    num_test = X.shape[0] # 500
    num_train = self.X_train.shape[0] # 5,000
    dists = np.zeros((num_test, num_train)) # (500,5000)
    #########################################################################
    # TODO:                                                                 #
    # Compute the l2 distance between all test points and all training      #
    # points without using any explicit loops, and store the result in      #
    # dists.                                                                #
    #                                                                       #
    # You should implement this function using only basic array operations; #
    # in particular you should not use functions from scipy.                #
    #                                                                       #
    # HINT: Try to formulate the l2 distance using matrix multiplication    #
    #       and two broadcast sums.                                         #
    #########################################################################
    M = np.dot(X, self.X_train.T)
    te = np.square(X).sum(axis = 1)
    # print te.shape, X.shape # (500,) (500,3072)
    tr = np.square(self.X_train).sum(axis = 1)
    # print tr.shape, self.X_train.shape # (5000,) (5000,3072)
    dists = np.sqrt(-2*M+tr+np.matrix(te).T)
    #########################################################################
    #                         END OF YOUR CODE                              #
    #########################################################################
    return dists

  def predict_labels(self, dists, k=1):
    """
    Given a matrix of distances between test points and training points,
    predict a label for each test point.

    Inputs:
    - dists: A numpy array of shape (num_test, num_train) where dists[i, j]
      gives the distance betwen the ith test point and the jth training point.

    Returns:
    - y: A numpy array of shape (num_test,) containing predicted labels for the
      test data, where y[i] is the predicted label for the test point X[i].
    """
    num_test = dists.shape[0] # 500
    y_pred = np.zeros(num_test) # (500)
    for i in xrange(num_test): # iterate 500 times
      # A list of length k storing the labels of the k nearest neighbors to
      # the ith test point.
      closest_y = []
      #########################################################################
      # TODO:                                                                 #
      # Use the distance matrix to find the k nearest neighbors of the ith    #
      # testing point, and use self.y_train to find the labels of these       #
      # neighbors. Store these labels in closest_y.                           #
      # Hint: Look up the function numpy.argsort.                             #
      #########################################################################
      labels = self.y_train[np.argsort(dists[i,:])].flatten() # (5000,)
      # np.argsort() 는 Returns the indices that would sort an array!
      closest_y = labels[0:k]
      #########################################################################
      # TODO:                                                                 #
      # Now that you have found the labels of the k nearest neighbors, you    #
      # need to find the most common label in the list closest_y of labels.   #
      # Store this label in y_pred[i]. Break ties by choosing the smaller     #
      # label.                                                                #
      #########################################################################
      c = Counter(closest_y)
      y_pred[i] = c.most_common(1)[0][0]
      # ex) c.most_common(5)은 가장 많이 나오는 (원소, 빈도수) tuple 5개를 반환한다.
      # Counter(words).most_common(5)
      # [('the', 1143), ('and', 966), ('to', 762), ('of', 669), ('i', 631)]
      #########################################################################
      #                           END OF YOUR CODE                            #
      #########################################################################

    return y_pred
