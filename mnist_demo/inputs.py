import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

def create_train_input_fn(train_config, train_input_config):
    mnist = input_data.read_data_sets(train_input_config.input_file_path, one_hot=True)
    _train_input_fn = tf.estimator.inputs.numpy_input_fn(
        x={'image': mnist.train.images},
        y=mnist.train.labels,
        batch_size=train_config.batch_size,
        shuffle=train_input_config.shuffle
    )

    return _train_input_fn

def create_eval_input_fn(eval_config, eval_input_config):
    mnist = input_data.read_data_sets(eval_input_config.input_file_path, one_hot=True)
    _train_input_fn = tf.estimator.inputs.numpy_input_fn(
        x={'image': mnist.train.images},
        y=mnist.train.labels,
        batch_size=eval_config.batch_size,
        shuffle=eval_input_config.shuffle
    )

def create_predict_input_fn():
    def _predict_input_fn():
        mnist = input_data.read_data_sets('MNIST_data/', one_hot=True)
        return mnist.test

    return _predict_input_fn


