# -*- coding: utf8 -*-
import numpy as np
from past.builtins import xrange

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
      dists = self.compute_distances_no_loops(X) # (500, 5000)
    elif num_loops == 1:
      dists = self.compute_distances_one_loop(X) # (500, 5000)
    elif num_loops == 2:
      dists = self.compute_distances_two_loops(X) # (500, 5000)
    else:
      raise ValueError('Invalid value %d for num_loops' % num_loops)

    return self.predict_labels(dists, k=k)

  def compute_distances_two_loops(self, X):
    """
    Compute the distance between each test point in X and each training point
    in self.X_train using a nested loop over both the training data and the 
    test data.

    Inputs:
    - X: A numpy array of shape (num_test, D) containing test data. # (500,3072)

    Returns:
    - dists: A numpy array of shape (num_test, num_train) where dists[i, j]
      is the Euclidean distance between the ith test point and the jth training
      point.
    """
    num_test = X.shape[0] # 500
    num_train = self.X_train.shape[0] # 5000
    dists = np.zeros((num_test, num_train)) # (500, 5000)
    for i in xrange(num_test): # 500회 반복
      for j in xrange(num_train): # 5,000회 반복
        #####################################################################
        # TODO:      
        # 2번의 loop을 통해 모든 테스트셋과 트레이닝셋 이미지들을
        #  비교 (500x5,000=250,000회) 하여 각각의 L2 dists 계산
        # Compute the l2 distance between the ith test point and the jth    #
        # training point, and store the result in dists[i, j]. You should   #
        # not use a loop over dimension.                                    #
        #####################################################################
        dists[i,j] = np.sqrt(np.sum((X[i] - self.X_train[j])**2))
        #dists[i,j] = np.linalg.norm(X[i] - self.X_train[j])
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
    num_train = self.X_train.shape[0] # 5000
    dists = np.zeros((num_test, num_train)) # (500, 5000)
    for i in xrange(num_test): # 500회 반복
      #######################################################################
      # TODO:   
      # 1번의 loop을 통해 모든 테스트셋과 트레이닝셋 이미지들을
      #  비교 (500x5,000=250,000회) 하여 각각의 L2 dists 계산
      # Compute the l2 distance between the ith test point and all training #
      # points, and store the result in dists[i, :].                        #
      #######################################################################
      #dists[i,:] = np.linalg.norm(self.X_train - X[i,:], axis=1)
      dists[i, :] = np.sqrt(np.sum((X[i] - self.X_train)**2, axis=1)) # broadcasting 이용
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
    num_train = self.X_train.shape[0] # 5000
    dists = np.zeros((num_test, num_train)) # (500, 5000)
    #########################################################################
    # TODO:                
    # Loop 없이 모든 테스트셋과 트레이닝셋 이미지들을
    #  비교 (500x5,000=250,000회) 하여 각각의 L2 dists 계산
    # Compute the l2 distance between all test points and all training      #
    # points without using any explicit loops, and store the result in      #
    # dists.                                                                #
    #                                                                       #
    # You should implement this function using only basic array operations; #
    # in particular you should not use functions from scipy.                #
    #                                                                       #
    # HINT: Try to formulate the L2 distance using matrix multiplication    #
    #       and two broadcast sums.                                         #
    #########################################################################
    
    dists = np.sqrt(np.sum(X**2, axis=1)[np.newaxis].T  # np.newaxis is adding one more axis. # (500,1)
                    -2*X.dot(self.X_train.T) # (500, 3072)dot(3072, 5000) = (500, 5000)
                    + np.sum(self.X_train**2, axis=1)) # (5000,)
    
    #M = np.dot(X, self.X_train.T)
    #te = np.square(X).sum(axis=1)
    # print (te.shape, X.shape) # (500,) (500,3072)
    #tr = np.square(self.X_train).sum(axis=1)
    # print (tr.shape, self.X_train.shape) # (5000,) (5000,3072)
    #dists = np.sqrt(-2*M + tr + np.matrix(te).T)
    
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
    
    # print (dists.shape) # (500, 5000)
    num_test = dists.shape[0] # 500
    y_pred = np.zeros(num_test) # 500
    for i in xrange(num_test):
      # A list of length k storing the labels of the k nearest neighbors to
      # the ith test point.
      closest_y = []
      #########################################################################
      # TODO:                                    
      # k개의 가장 가까운 클래스 추출해 주기
      # Use the distance matrix to find the k nearest neighbors of the ith    #
      # testing point, and use self.y_train to find the labels of these       #
      # neighbors. Store these labels in closest_y.                           #
      # Hint: Look up the function numpy.argsort.
      #########################################################################
      closest_y = self.y_train[dists[i].argsort()[:k]] 
      # ex) dists[0]의 5000개의 distance를 가장 작은 것부터 정렬한 다음에 그중 k개의 인덱스를 반환 (ex: 3216) 한 후 y_train[3216] 해서 클래스 추출
      # if k = 1 : integer (0~9), if k = 5 : [6 2 4 4 4] 
      #########################################################################
      # TODO:                                    
      # k개 간에 다수결로 하나의 최종 클래스 결정해 주기
      # Now that you have found the labels of the k nearest neighbors, you    #
      # need to find the most common label in the list closest_y of labels.   #
      # Store this label in y_pred[i]. Break ties by choosing the smaller     #
      # label.                                                                #
      #########################################################################
      y_pred[i] = np.argmax(np.bincount(closest_y))
      #########################################################################
      #                           END OF YOUR CODE                            # 
      #########################################################################

    return y_pred

