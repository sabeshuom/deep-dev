import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import math

log_dir = "/home/sabesan/deep-tmv/dev/tutorial/log"
data_dir = "/home/sabesan/deep-tmv/dev/tutorial/data/mnist"

MAX_STEPS = 1000
NO_OF_CLASSES = 10
IMAGE_SIZE = 28
IMAGE_PIXELS = IMAGE_SIZE * IMAGE_SIZE
BATCH_SIZE = 100
LEARNING_RATE = 0.01
HIDDEN1_UNITS = 128
HIDDEN2_UNITS = 32
sess = tf.InteractiveSession()

data = input_data.read_data_sets(data_dir, one_hot = True)
# data has train.next_batch(xx) test.images. test.labels
with tf.name_scope('input') as scope:
    x = tf.placeholder(tf.float32, [None, IMAGE_PIXELS], name='images-in')
    y_ = tf.placeholder(tf.float32, [None, NO_OF_CLASSES], name = 'lables-in')

with tf.name_scope('hidden1') as scope:
    h1_w = tf.Variable(tf.truncated_normal([IMAGE_PIXELS, HIDDEN1_UNITS],\
                                           stddev=1.0 / math.sqrt(float(HIDDEN1_UNITS)), name="weights"))
    h1_b = tf.Variable(tf.zeros([HIDDEN1_UNITS]), name = 'bias')                                         
    h1 = tf.nn.relu(tf.matmul(x, h1_w) + h1_b)

with tf.name_scope('hidden2') as scope:
    h2_w = tf.Variable(tf.truncated_normal([HIDDEN1_UNITS, HIDDEN2_UNITS],\
                                           stddev=1.0 / math.sqrt(float(HIDDEN2_UNITS)), name="weights"))
    h2_b = tf.Variable(tf.zeros([HIDDEN2_UNITS]), name = 'bias')                                         
    h2 = tf.nn.relu(tf.matmul(h1, h2_w) + h2_b)

with tf.name_scope('softmax') as scope:
    b = tf.Variable(tf.zeros([NO_OF_CLASSES]), name= 'bias')
    W = tf.Variable(tf.truncated_normal([HIDDEN2_UNITS, NO_OF_CLASSES], \
                                        stddev=1.0 /math.sqrt(float(HIDDEN2_UNITS))), name='weight') 
    y = tf.nn.softmax(tf.matmul(h2, W) + b)

with tf.name_scope('training') as scope:
    ce = -tf.reduce_sum(y_* tf.log(y))
    tf.scalar_summary('cross entrophy', ce)
    train_step = tf.train.GradientDescentOptimizer(LEARNING_RATE).minimize(ce)

with tf.name_scope('testing') as scope:
    cp = tf.equal(tf.arg_max(y,1), tf.arg_max(y_,1))
    accuracy = tf.reduce_mean(tf.cast(cp, tf.float32))

tf.scalar_summary('accuracy', accuracy)

ms = tf.merge_all_summaries()
writer = tf.train.SummaryWriter(log_dir, sess.graph.as_graph_def(add_shapes= True))

tf.initialize_all_variables().run()


for i in range(MAX_STEPS):
    batch_x, batch_y = data.train.next_batch(BATCH_SIZE)
    feed = {x: batch_x, y_:batch_y}
    sess.run(train_step, feed_dict=feed)
    
    if(i%10 ==0):
        feed = {x:data.test.images, y_: data.test.labels}
        res = sess.run([ms, accuracy], feed_dict=feed)
        print('Accuracy at %d : %f' % (i, res[1]))
        writer.add_summary(res[0], i)
