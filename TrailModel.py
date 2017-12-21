import tensorflow as tf
import numpy as np
class Trail():
     def __init__(self,source_vocab_size,embeding_size,num_layers,rnn_size,learning_rate,mode='train'):
         self.source_vocab_size=source_vocab_size
         self.embedding_size=embeding_size
         self.num_layers=num_layers
         self.rnn_size=rnn_size
         self.learning_rate=learning_rate
         self.mode=mode
         self.inputs1=tf.placeholder(tf.int32,[None,None],name='inputs1')
         self.inputs2=tf.placeholder(tf.int32,[None,None],name='inputs2')
         self.sequence_length1=tf.placeholder(tf.int32,[None],name='sequence_length1')
         self.sequence_length2=tf.placeholder(tf.int32,[None],name='sequence_length2')
         self.labels=tf.placeholder(tf.int32,[None,2],name='labels')
         self.W=tf.get_variable(shape=[self.rnn_size*2,2],initializer=tf.random_normal_initializer(stddev=0.1),name='W')
         self.b=tf.Variable(tf.constant(0.1, shape=[2]), name="b")
         # embeding层
         self.embeding=tf.Variable(tf.random_uniform([self.source_vocab_size,self.embedding_size],-1.0,1.0),name='embeding')
         self.embeding_layers1=self.embeding_layers(self.inputs1)
         self.embeding_layers2=self.embeding_layers(self.inputs2)
         #两个lstm层
         self.lstm_layer1=self.get_lstm_layers(self.embeding_layers1,self.sequence_length1,"lstm1",self.rnn_size)
         self.lstm_layer2 = self.get_lstm_layers(self.embeding_layers2, self.sequence_length2,"lstm2",self.rnn_size)
         #lstm连接层
         self.layers_concat=tf.concat([self.lstm_layer1,self.lstm_layer2],1)
         #全连接层
         self.logits=self.get_logits()
         self.prediction=tf.argmax(self.logits,1)
         #网络训练方法
         self.loss=tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=self.labels, logits=self.logits))
         self.train_op = tf.train.AdamOptimizer(learning_rate=self.learning_rate).minimize(self.loss)

         #validtion验证准确率
         self.accuracy=self.get_accuary()

     def embeding_layers(self,input_data):
        embeding_word = tf.nn.embedding_lookup(self.embeding,input_data)
        return embeding_word

     def get_lstm_layers(self,embeding_layers,source_sequence_length,name,rnn_size):
        with tf.variable_scope(name):
            temp=[]
            for _ in range(self.num_layers):
                lstm_cell = tf.contrib.rnn.LSTMCell(rnn_size)
                #lstm中的drop机制
                if(self.mode=='train'):
                    self.drop_prob = tf.placeholder(tf.float32, name='dropout')
                    lstm_cell=tf.contrib.rnn.DropoutWrapper(lstm_cell, output_keep_prob=self.drop_prob)
                elif(self.mode=='inference'):
                    lstm_cell=lstm_cell
                temp.append(lstm_cell)
            ce = tf.contrib.rnn.MultiRNNCell(temp)
            encoder_output, encoder_state = tf.nn.dynamic_rnn(ce, embeding_layers,sequence_length=source_sequence_length,dtype=tf.float32)
            res_state=encoder_state[0][1]       #[batch_szie,rnn_size]
        return res_state
     def get_logits(self):
         logits=tf.nn.xw_plus_b(self.layers_concat,self.W,self.b)
         return logits
     def get_accuary(self):
         correct_predictions = tf.equal(self.prediction, tf.argmax(self.labels, 1))
         accuracy = tf.reduce_mean(tf.cast(correct_predictions, "float"), name="accuracy")
         return accuracy