import numpy as np
import random
import libpyAI as ai

OUTPUT=0
def perceptron(inputs):
	output = sum(inputs)
	if output == 5:
		return 1
	return 0

def step(x):
  if x >= 0:
    return 1
  return 0

def train(inputs, epoch=1000, learning_rate=0.1):
    inputs = np.asarray(inputs)
    
    weights = np.random.rand(1,5) - 0.5    
    threshold = -1
    desired_output = perceptron(inputs)

    for i in range(epoch):
      output = np.sum(inputs * weights) - threshold  #now it's threshold's weight
      error = desired_output - (step(output))
      threshold = - learning_rate * error   #now it's threshold's weight
      delta = inputs * learning_rate * error
      weights = weights + delta

    output = np.sum(inputs * weights) - threshold
    return step(output)

OUTPUT=train([1, 1, 1, 1, 1])
