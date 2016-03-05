from tensorflow.examples.tutorials.mnist import input_data

log_dir = "/home/sabesan/deep-tmv/dev/tutorial/log"
data_dir = "/home/sabesan/deep-tmv/dev/tutorial/data/mnist"

mnist = input_data.read_data_sets(data_dir, one_hot=True)

import tensorflow as tf
sess  = tf.InteractiveSession()

def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)

def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)

def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')
  
def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                           strides=[1, 2, 2, 1], padding='SAME')

with tf.name_scope('input') as scope:
    x = tf.placeholder(tf.float32, [None, 784])
    y_ = tf.placeholder(tf.float32, [None, 10])
    x_image = tf.reshape(x, [-1,28,28,1])

with tf.name_scope('conv1') as scope:
    W_conv1 = weight_variable([5, 5, 1, 32])
    b_conv1 = bias_variable([32])
    h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)

with tf.name_scope('maxpool1') as scope:
    h_pool1 = max_pool_2x2(h_conv1)    

tf.image_summary('conv1- weights',tf.reshape(W_conv1, [32, 5, 5, 1]), max_images=200)


with tf.name_scope('conv2') as scope:
    W_conv2 = weight_variable([5, 5, 32, 64])
    b_conv2 = bias_variable([64])
    h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)

with tf.name_scope('maxpool2') as scope:
    h_pool2 = max_pool_2x2(h_conv2)

tf.image_summary('conv2- weights',tf.reshape(W_conv2, [32*64, 5, 5, 1]), max_images=200)

with tf.name_scope('fc') as scope:
    W_fc1 = weight_variable([7 * 7 * 64, 1024])
    b_fc1 = bias_variable([1024])
    
    h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64])
    h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

with tf.name_scope('dropout') as scope:
    keep_prob = tf.placeholder(tf.float32)
    h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

with tf.name_scope('softmax') as scope:
    W_fc2 = weight_variable([1024, 10])
    b_fc2 = bias_variable([10])
    y_conv=tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)

with tf.name_scope('training') as scope:
    cross_entropy = -tf.reduce_sum(y_*tf.log(y_conv))
    train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

with tf.name_scope('testing') as scope:    
    correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_,1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

tf.scalar_summary('Accuracy', accuracy)

ms = tf.merge_all_summaries()
writer = tf.train.SummaryWriter(log_dir, sess.graph.as_graph_def(add_shapes= True))


sess.run(tf.initialize_all_variables())

for i in range(20000):
  images, labels = mnist.train.next_batch(50)
  train_step.run(feed_dict={x: images, y_: labels, keep_prob: 0.5})

  if i%100 == 0:
    #train_accuracy = accuracy.eval(feed_dict={ x:batch[0], y_: batch[1], keep_prob: 1.0})
    #print("step %d, training accuracy %g"%(i, train_accuracy))
    res = sess.run([ms, accuracy], feed_dict={ x:mnist.test.images, y_: mnist.test.labels, keep_prob: 1.0})
    print('Accuracy at %d : %f' % (i, res[1]))
    writer.add_summary(res[0], i)
