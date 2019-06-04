import tensorflow as tf

class FullConnect(object):
    def __init__(self, config):
        self._config = config

    def predict(self, inputs):
        config = self._config
        logits = tf.keras.layers.Dense(config.output_units)(inputs)
        return logits

    def loss(self, predictions, labels):
        loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=predictions, logits=labels))
        return loss

    def format_output(self, predictions):
        return tf.arg_max(predictions)

