import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
log_dir = "/../../log/tutorial/t1_softmax"
data_dir = "../../data/tutorial/mnist"

MAX_STEPS = 1000
NO_OF_CLASSES = 10
IMAGE_SIZE = 28
IMAGE_PIXELS = IMAGE_SIZE * IMAGE_SIZE
BATCH_SIZE = 100
LEARNING_RATE = 0.01
sess = tf.InteractiveSession()

data = input_data.read_data_sets(data_dir, one_hot = True)
# data has train.next_batch(xx) test.images. test.labels
with tf.name_scope('input') as scope:
    x = tf.placeholder(tf.float32, [None, IMAGE_PIXELS], name='images-in')
    y_ = tf.placeholder(tf.float32, [None, NO_OF_CLASSES], name = 'lables-in')

with tf.name_scope('softmax') as scope:
    b = tf.Variable(tf.zeros([NO_OF_CLASSES]), name= 'bias')
    W = tf.Variable(tf.zeros([IMAGE_PIXELS, NO_OF_CLASSES]), name='weight') 
    Wx_b = tf.matmul(x,W) + b
    y = tf.nn.softmax(Wx_b) 
    
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
