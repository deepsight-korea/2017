# -*- coding: utf8 -*-
from __future__ import print_function

import numpy as np
from random import shuffle
from past.builtins import xrange

#######################################################
################### 함수1 (naive) ######################
#######################################################

def svm_loss_naive(W, X, y, reg):
  """
  
  W, X, y, reg를 인자로 받아서
  loss와 dW를 계산하여 반환해 주면 됨
  
  DW 구하는 방법
  http://cs231n.github.io/optimization-1/#gradcompute 에 나와있음.
  간단히 말하자면 
  
  Structured SVM loss function, naive implementation (with loops).

  Inputs have dimension D, there are C classes, and we operate on minibatches
  of N examples.
  
  D = 차원 (=3073)
  N = 미니배치 개수 (=500)
  C = 클래스 개수 (=10)

  Inputs:
  - W: A numpy array of shape (D, C) containing weights.
  - X: A numpy array of shape (N, D) containing a minibatch of data.
  - y: A numpy array of shape (N,) containing training labels; y[i] = c means 
    that X[i] has label c, where 0 <= c < C.
  - reg: (float) regularization strength
  
  y는 X의 레이블임 (ground truth)
  
  전달받은 인자 (dev의 경우)
  - W (3073,10)
  - X (500,3073)
  - y (500,)
  - reg 0.00001

  Returns a tuple of:
  - loss as single float
  - gradient with respect to weights W; an array of same shape as W
  
  반환할 놈 : (loss, gradient) 의 tuple
      - loss : 실수 (스칼라)
      - gradient (=dW) : 당연히 W와 동일한 shape을 가져야 함  
      
  SVM Loss
  
  Li = sum(max(0, Sj - Sy + 1) (j != y)
  L = sum(Li) / N (N은 학습 이미지의 갯수) (클래스의 갯수 아님)
      
  """

  # 일단 loss와 gradient 초기화해 주면서 시작해 보자.

  # loss를 초기화 (스칼라값. 0으로)
  loss = 0.0

  # Gradient (dW) 를 초기화 (W와 동일한 shape을 가지며 모든 원소는 0)
  dW = np.zeros(W.shape) # initialize the gradient as zero # (3073,10)

  # 이제 loss와 gradient (dW) 를 계산하자 (compute the loss and the gradient)

  num_classes = W.shape[1] # 10
  num_train = X.shape[0] # 500 (dev의 경우)
  
  for i in xrange(num_train): # 500회 반복 (dev의 경우)
    scores = X[i].dot(W) # (1,3073) x (3073,10) = (1,10) ----> X[i]는 (500, 3073) 이 아니라 (1, 3073) 이 됨에 유의
    # print (scores) # (1,10) 의 차원을 가지게 된다. 
    # [-0.2817172  -0.63071491  0.3409894   0.05924502 -0.42442256 -0.09732553 0.25105701  0.45409751  0.57843647  0.7573004 ]
    correct_class_score = scores[y[i]]
    # print (y[i]) # correct label이다 # i=0 일때 y[i]:  5
    # print (scores[y[i]]) # correct label인 경우의 점수 # i=0 일때 y[i]=5니까 6번째 원소값인 -0.097325532079
    # print (correct_class_score) # 당연히 동일하게 -0.097325532079
    for j in xrange(num_classes): # 10회 반복
      if j == y[i]:
        continue
      margin = scores[j] - correct_class_score + 1 # note delta = 1
      if margin > 0:
        loss += margin
        # Wyi 의 gradient
        dW[:, y[i]] -= X[i, :].T # j==y : accumulate the gradient over incorrect classes to the correct class weight vector
        # Wj의 gradient
        dW[:, j]    += X[i, :].T # j!=y : incorrect class weight vector gradient

  # Right now the loss is a sum over all training examples, but we want it
  # to be an average instead so we divide by num_train.
  loss /= num_train

  # same for gradients
  dW /= num_train

  # Add regularization to the loss.
  # loss += 0.5 * reg * np.sum(W * W)  # W*W is elementwise computation. WHY 0.5?
  loss += reg * np.sum(W * W)

  #############################################################################
  # TODO:                                                                     #
  # Compute the gradient of the loss function and store it dW.                #
  # Rather that first computing the loss and then computing the derivative,   #
  # it may be simpler to compute the derivative at the same time that the     #
  # loss is being computed. As a result you may need to modify some of the    #
  # code above to compute the gradient.                                       #
  #############################################################################
  
  dW += reg*W # 이 라인 추가!

  return loss, dW


#######################################################
################ 함수2 (vectorized) ####################
#######################################################

def svm_loss_vectorized(W, X, y, reg):
  """
  Structured SVM loss function, vectorized implementation.

  Inputs and outputs are the same as svm_loss_naive.
  """
  loss = 0.0
  dW = np.zeros(W.shape) # initialize the gradient as zero

  #############################################################################
  # TODO:                                                                     #
  # Implement a vectorized version of the structured SVM loss, storing the    #
  # result in loss.                                                           #
  #############################################################################
  num_train = X.shape[0] # 500
  num_classes = W.shape[1] # 10
  D = X.shape[1]

  scores = X.dot(W) # (500, 3073).(3073, 10) = (500, 10)
  correct_class_score = scores[np.arange(num_train),y] # (500,)
  margins = (scores.T - correct_class_score + 1).T
  margins[np.arange(num_train), y] = 0 # correct class
  margins[margins<0] = 0 # negative number is changed to 0
  loss = np.sum(margins)
  loss /= num_train
  # loss += 0.5 * reg * np.sum(W * W)
  loss += reg * np.sum(W * W)
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################


  #############################################################################
  # TODO:                                                                     #
  # Implement a vectorized version of the gradient for the structured SVM     #
  # loss, storing the result in dW.                                           #
  #                                                                           #
  # Hint: Instead of computing the gradient from scratch, it may be easier    #
  # to reuse some of the intermediate values that you used to compute the     #
  # loss.                                                                     #
  #############################################################################
  binary = margins # binary = mask
  binary[margins>0] = 1
  row_sum = np.sum(binary, axis=1)
  binary[range(num_train), y] = -row_sum
  dW = binary.T.dot(X).T
  dW /= num_train

  dW += reg*W
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################

  return loss, dW
