# Delta Recurrent Neural Network (Delta-RNN) Framework
#
# This gives an implementation of the Delta-RNN framework given in Ororbia et al. 2017, arXiv:1703.08864 [cs.CL], 
# https://arxiv.org/abs/1703.08864 using Python and Tensorflow.
#
# This code implements a variety of RNN models using the Delta-RNN Framework
#
# Stuart Hagler, 2017

# Imports
import tensorflow as tf

# Local imports
from delta_rnn import delta_rnn_graph

# Define derived GRU TensorFlow graph class
class gru_graph(delta_rnn_graph):
    
    # Graph constructor
    def __init__(self, num_gpus, alpha, c_size, h_size, vocabulary_size, num_training_unfoldings, 
                 num_validation_unfoldings, training_batch_size, validation_batch_size, optimization_frequency):
        
        # Feed remaining hyperparameters to delta RNN __init__
        delta_rnn_graph.__init__(self, num_gpus, h_size, h_size, vocabulary_size, num_training_unfoldings,
                                 num_validation_unfoldings, training_batch_size, validation_batch_size, 
                                 optimization_frequency)
        
    # GRU cell definition
    def _cell(self, x, c, h):
        with tf.name_scope('z'):
            z = tf.sigmoid(tf.matmul(x, self._Wz) + tf.matmul(h, self._Vz) + self._bz)
        with tf.name_scope('r'):
            r = tf.sigmoid(tf.matmul(x, self._Wr) + tf.matmul(h, self._Vr) + self._br)
        with tf.name_scope('c'):
            c = tf.matmul(x, self._Wh) + tf.matmul(r*h, self._Vh) + self._bh
        with tf.name_scope('h'):
            h = z*h + (1-z)*tf.tanh(c)
        with tf.name_scope('o'):
            o = tf.nn.xw_plus_b(h, self._W, self._b)
        return o, c, h
    
    # Setup GRU cell parameters
    def _setup_cell_parameters(self):     
        with tf.name_scope('Wz'):
            self._Wz = tf.Variable(tf.truncated_normal([self._vocabulary_size, self._h_size], -0.1, 0.1))         
        with tf.name_scope('Vz'):
            self._Vz = tf.Variable(tf.truncated_normal([self._h_size, self._h_size], -0.1, 0.1))         
        with tf.name_scope('bz'):
            self._bz = tf.Variable(tf.zeros([1, self._h_size]))         
        with tf.name_scope('Wr'):
            self._Wr = tf.Variable(tf.truncated_normal([self._vocabulary_size, self._h_size], -0.1, 0.1))         
        with tf.name_scope('Vr'):
            self._Vr = tf.Variable(tf.truncated_normal([self._h_size, self._h_size], -0.1, 0.1))         
        with tf.name_scope('br'):
            self._br = tf.Variable(tf.zeros([1, self._h_size]))        
        with tf.name_scope('Wh'):
            self._Wh = tf.Variable(tf.truncated_normal([self._vocabulary_size, self._h_size], -0.1, 0.1))         
        with tf.name_scope('Vh'):
            self._Vh = tf.Variable(tf.truncated_normal([self._h_size, self._h_size], -0.1, 0.1))        
        with tf.name_scope('bh'):
            self._bh = tf.Variable(tf.zeros([1, self._h_size]))        
        with tf.name_scope('W'):
            self._W = tf.Variable(tf.truncated_normal([self._h_size, self._vocabulary_size], -0.1, 0.1))        
        with tf.name_scope('b'):
            self._b = tf.Variable(tf.zeros([self._vocabulary_size]))