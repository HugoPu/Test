import tensorflow as tf

class FullConnect(object):
    def __init__(self, config, is_training, add_summary):
        self._config = config

    def predict(self, inputs):
        config = self._config
        logits = tf.keras.layers.Dense(config.num_units)(inputs)
        return logits

    def loss(self, predictions, labels):
        # loss = -tf.reduce_sum(labels * tf.log(predictions))
        loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=predictions, labels=labels))
        return loss

    def format_output(self, predictions):
        return tf.arg_max(predictions, 1)

