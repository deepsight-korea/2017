import numpy as np
from random import shuffle

def softmax(f_scores):
    f_scores = np.matrix(f_scores) # [[ 10.   5.   5.]] # ndim : 2
    f_prob = np.exp(f_scores)/np.vstack( np.sum(np.exp(f_scores), axis=1) )
    # print np.exp(f_scores) # [[ 22026.46579481    148.4131591     148.4131591 ]] 
    # print np.sum(np.exp(f_scores)) # 22323.292113
    # ??? WHY include np.vstack()? Even if we remove it, the code seems to be working well like below!
    # f_prob = np.exp(f_scores)/np.sum(np.exp(f_scores), axis=1)
    return f_prob

def softmax_loss_naive(W, X, y, reg):
  """
  Softmax loss function, naive implementation (with loops)

  Inputs have dimension D, there are C classes, and we operate on minibatches
  of N examples.

  Inputs:
  - W: A numpy array of shape (D, C) containing weights.
  - X: A numpy array of shape (N, D) containing a minibatch of data.
  - y: A numpy array of shape (N,) containing training labels; y[i] = c means
    that X[i] has label c, where 0 <= c < C.
  - reg: (float) regularization strength

  Returns a tuple of:
  - loss as single float
  - gradient with respect to weights W; an array of same shape as W
  """
  # Initialize the loss and gradient to zero.
  loss = 0.0
  dW = np.zeros_like(W) # create an array which has the same shape as W. All elements are zeros.
  num_classes = W.shape[1] # 10
  num_train = X.shape[0] # X_dev : 500, X_train : 49000
    
  #############################################################################
  # TODO: Compute the softmax loss and its gradient using explicit loops.     #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################

  for i in range(num_train): # X_dev : 500 loops, X_train : 49,000 loops
    f_scores = X[i].dot(W) # (3072,).dot(3072,10) = (10,)
    f_scores -= np.max(f_scores) # for numerical stability # (10,) # 0 or negative number
    # ex) [-0.79737468 -0.10509648 -0.88453138  0. -0.86025529 -0.73945449 -0.3267534  -1.10335502 -0.94237021 -0.67619172]
    
    # Softmax probabilities 
    p = np.exp(f_scores)/np.sum(np.exp(f_scores)) # (10,) # Yes, it works okay without np.vstack()
    # ex) [ 0.08022826 0.16031715 0.07353189 0.17808314 0.0753388 0.08501231 0.12844453 0.05908018 0.06939955 0.09056419]
    
    # Cross entropy loss
    loss += -np.log(p[y[i]]) # adds 500 times. Final loss is a float which accumulates 500 losses.
    # ex) 1.75221261568 -> 4.29898383038 -> 6.62357399912 -> ... -> 1178.76373326 -> 1181.48800106 -> 1183.82750017 (500 times)
    
    for j in range(num_classes): # 10 loops
        # Gradient 
        # Ref: http://nbviewer.jupyter.org/github/yrevar/machine_learning_blog/blob/draft/softmax_gradient_derivation/softmax_gradient_derivation.ipynb
        dW[:,j] += (p[j] - (j==y[i]))*X[i,:]

  # Compute average
  loss /= num_train
  dW /= num_train

  # Regularization
  loss += 0.5*reg*np.sum(W*W)
  dW += reg*W
  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################

  return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
  """
  Softmax loss function, vectorized version.

  Inputs and outputs are the same as softmax_loss_naive.
  """
  # Initialize the loss and gradient to zero.
  loss = 0.0
  dW = np.zeros_like(W)
  num_classes = W.shape[1]
  num_train = X.shape[0]
    
  #############################################################################
  # TODO: Compute the softmax loss and its gradient using no explicit loops.  #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################
  f_scores = X.dot(W) # same (3072,).dot(3072,10) = (10,)
  f_scores -= np.max(f_scores, axis=1, keepdims=True) # for numerical stability # (10,) # 0 or negative number
  # f_scores -= np.max(f_scores) # naive version
    
  # Softmax probabilities
  p = np.exp(f_scores)/np.sum(np.exp(f_scores), axis=1, keepdims=True) # (10,)
  # p = np.exp(f_scores)/np.sum(np.exp(f_scores)) # naive version
  
  # Cross entropy loss
  loss = -np.mean(np.log(p[range(num_train),y]))
  # loss += -np.log(p[y[i]]) # slight different with naive version because of this computation is vectorized

  # Add regularization to the loss
  loss += 0.5*reg*np.sum(W*W)


  # we want p[j] - 1 for when j == y[i], otherwise p[j] - 0
  # Prepare a zero matrix of shape p and assign 1 to elements where p[j] == y[i] 
  p[range(num_train), y] -= 1

  # Gradient of the loss
  dW = np.dot(X.T, p) 
  dW /= num_train # gradient of the data loss
  dW += reg*W # gradient of the regularization loss
  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################
  return loss, dW

