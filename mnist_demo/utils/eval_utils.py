import tensorflow as tf


def get_eval_metrics_ops_for_evaluatiors(eval_config, predictions, labels):
    eval_metric_ops = {'accuracy': tf.metrics.accuracy(tf.arg_max(labels, 1), predictions)}
    return eval_metric_ops