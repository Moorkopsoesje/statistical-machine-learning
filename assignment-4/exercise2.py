# -*- coding: utf-8 -*-
# Guido Zuidhof s4160703
# Iñez Wijnands s4149696
# SML ASS 4 exercise2.py
from __future__ import division
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
from scipy.stats import multivariate_normal
from mpl_toolkits.mplot3d import Axes3D
import random
from tqdm import tqdm


#Gaussian
def ex1_gaussian(x):
    sigma = 0.4 * np.identity(2)

    return 3 * multivariate_normal.pdf(x,[0,0],sigma)

def plot_gaussian(data_function, a_space, b_space, name):
    X, Y = np.meshgrid(a_space, b_space)
        
    z = np.array( [data_function([x,y]) for x,y in zip(np.ravel(X),np.ravel(Y))])
    Z = z.reshape(X.shape)
    
    #Plot
    fig = plt.figure(0)
    ax = fig.add_subplot(111, projection='3d')
    plt.xlabel(r'$x_1$')
    plt.ylabel(r'$x_2$')
    
    surf = ax.plot_surface(X,Y, Z, cmap=cm.winter, linewidth=0.05,rstride=2, cstride=2)
    
    fig.set_size_inches(10,7)
    fig.savefig(name, dpi=100)
    
def plot_gaussian_given(X, Y, Z, name, elev=45, azim=0):
        
    Z = np.array(Z).reshape(X.shape)
    
    #Plot
    fig = plt.figure(0)
    ax = fig.add_subplot(111, projection='3d')
    plt.xlabel(r'$x_1$')
    plt.ylabel(r'$x_2$')
    surf = ax.plot_surface(X,Y, Z, cmap=cm.winter, linewidth=0.05,rstride=2, cstride=2)
    ax.view_init(elev=elev, azim=azim)
    
    fig.set_size_inches(10,7)
    fig.savefig(name, dpi=100)    



def plot_standard_gaussian():
    x1_space = np.linspace(-2,2,40)
    x2_space = np.linspace(-2,2,40)
    
    plot_gaussian(ex1_gaussian, x1_space, x2_space, "std_iso_gaussian")



def forward_pass(w1, w2, X):
    
    X_with_bias = list(X) + [1]
    
    activations_hidden = []#np.zeros((len(w1),))
    
    for W in w1:
        weighted_sum = np.sum(np.dot(X_with_bias,W))
        activations_hidden.append(np.tanh(weighted_sum))
        
    #BIAS!
    activations_hidden += [1]
    
    output = np.sum( np.dot(activations_hidden, w2))
    return output, activations_hidden 
    
    
def backpropagation(w1, w2, activations, output, target, x, eta=0.1):
    d_k = output - target
    d_js = []
    
    delta_weights = []
    
    #BIAS!
    x = list(x) + [1]
    
    #Update hidden->output weights
    for activation, weight in zip(activations, w2):
        d_j = (1-activation**2) * weight * d_k
        d_js.append(d_j)
        
        delta_weight = d_k * activation
        delta_weights.append(delta_weight)
        
    
    
    w2 = w2 - eta * np.array(delta_weights)
    
    
    #Remove final element, BIAS
    d_js = d_js[:-1] 
    
    delta_weights = []
    
    #Update input->hidden weights
    for d_j in d_js:
        delta_weight = d_j * np.array(x)
        delta_weights.append(delta_weight)
    
    w1 = w1 - eta * np.array(delta_weights)
        
    return w1, w2
    
    

def create_weights(n_nodes):
    return np.random.rand(*n_nodes)-0.5
    
    
def create_nn(n_input_nodes=2, n_hidden_nodes=8, n_output_nodes=1):
    weights_1 = np.random.rand(n_hidden_nodes,n_input_nodes+1)-0.5
    weights_2 = np.random.rand(n_hidden_nodes+1)-0.5
    
    return weights_1, weights_2
    
#Network for part 2, 3, 4 (minor edits to code required for changing settings)
def run_nn():
    x1_space = np.linspace(-2,2,40)
    x2_space = np.linspace(-2,2,40)
    
    x_grid, y_grid = np.meshgrid(x1_space, x2_space)
    
    X = zip(np.ravel(x_grid),np.ravel(y_grid))
    Y = np.array( [ex1_gaussian([x1,x2]) for x1,x2 in X])
        
    weights_1, weights_2 = create_nn(n_hidden_nodes=4)
    
    outputs = np.zeros(Y.shape)
    
    indices = range(len(X))
    random.shuffle(indices)
    
    for i in tqdm(range(500)):
        outputs = np.zeros(Y.shape)
        
        for n, index in enumerate(indices):
            x = X[index]
            y = Y[index]
            
            out, activation = forward_pass(weights_1, weights_2, x)
            outputs[index] = out
            weights_1, weights_2 = backpropagation(weights_1, weights_2, activation, out, target=y, x=x, eta=0.1)
      
        #if i == 0:
        #    plot_gaussian_given(x_grid, y_grid, outputs, "ex2_2", elev=45, azim=45)
        #if i == 1:
        #    plot_gaussian_given(x_grid, y_grid, outputs, "ex2_2_1", elev=45, azim=45)
        if (i+1)%50 == 0:            
            plot_gaussian_given(x_grid, y_grid, outputs, "ex2_4lh_"+str(i+1), elev=45, azim=45)
            
        if (i+1)%10 == 0 and i < 101:
            plot_gaussian_given(x_grid, y_grid, outputs, "ex2_4lh_"+str(i+1), elev=45, azim=45)


#Network for part 6
def run_nn_6():
    data = np.loadtxt('a017_NNpdfGaussMix.txt')
    _x1, _x2, y = zip(*data)
    #x1 = np.array(x1)
    #x2 = np.array(x2)
    Y = np.array(y)
    
    x1_space = np.linspace(-2,2,41)
    x2_space = np.linspace(-2,2,41)
    
    x_grid, y_grid = np.meshgrid(x1_space, x2_space)
    
    #print len(y), len(x1), len(X), len(Y)
    #plot_gaussian_given(X, Y, y, "ex2_5")
    plot_gaussian_given(x_grid, y_grid, y, "ex2_5", elev=45, azim=45)
    
    X = zip(np.ravel(x_grid),np.ravel(y_grid))
    
    weights_1, weights_2 = create_nn(n_hidden_nodes=60, )
    
    outputs = np.zeros(Y.shape)
    
    for i in tqdm(range(2000)):
        outputs = np.zeros(Y.shape)
        indices = range(len(X))
        random.shuffle(indices)
        
        for n, index in enumerate(indices):
            x = X[index]
            y = Y[index]    
            
            out, activation = forward_pass(weights_1, weights_2, x)
            outputs[index] = out
            weights_1, weights_2 = backpropagation(weights_1, weights_2, activation, out, target=y, x=x, eta=0.001)
      
      
        if (i+1)%50 == 0:            
            plot_gaussian_given(x_grid, y_grid, outputs, "plot/ex2_6_"+str(i+1), elev=45, azim=45)

if __name__ == "__main__":
    np.random.seed(1)
    #plot_standard_gaussian()
    #run_nn()
    
    run_nn_6()
    
    
    print "yes yes yes girl"
