import tensorflow as tf
import copy
import functools

from mnist_demo.utils.config_utils import get_configs_from_pipeline_file
from mnist_demo.model.model_builder import build
from mnist_demo.inputs import create_eval_input_fn, create_predict_input_fn, create_train_input_fn

def create_model_fn(init_model_fn, configs, hparams):
    train_config = configs['train_config']
    eval_config = configs['eval_config']

    def model_fn(features, labels, mode, params=None):
        params = params or {}
        is_training = mode == tf.estimator.ModeKeys.TRAIN
        model = init_model_fn(is_training=is_training)

        predictions = model.predict(features)

        format_predictions = None
        if mode == tf.estimator.ModeKeys.PREDICT:
            format_predictions = model.format_output(predictions)

        loss = None
        train_op = None
        if mode == tf.estimator.ModeKeys.TRAIN:
            loss = model.loss(predictions, labels)
            optimizer = tf.train.AdagradDAOptimizer(learning_rate=train_config.lr)
            train_op = optimizer.minimize(loss, global_step=tf.train.get_global_step())

        return tf.estimator.EstimatorSpec(
            mode=mode,
            predictions=format_predictions,
            loss=loss,
            train_op=train_op
        )

    return model_fn


def create_estimator_and_inputs(run_config,
                                hparams,
                                pipeline_config_path,
                                config_override=None,
                                train_steps=None,
                                model_fn_creator=create_model_fn,
                                **kwargs):

    configs = get_configs_from_pipeline_file(pipeline_config_path,
                                             config_override=config_override)
    model_fn_base = build
    kwargs.update({
        'train_steps':train_steps
    })
    model_config = None
    train_config = configs['train_config']
    eval_config = configs['eval_config']
    train_input_config = configs['train_input_config']
    eval_input_config = configs['eval_input_config']

    if train_steps is None and train_config.num_steps != 0:
        train_steps = train_config.num_steps

    model_fn = functools.partial(model_fn_base, model_config=model_config)

    train_input_fn = create_train_input_fn(
        train_config=train_config,
        train_input_config=train_input_config
    )

    eval_input_fn = create_eval_input_fn(
        eval_config=eval_config,
        eval_input_config=eval_input_config
    )

    model_fn = model_fn_creator(model_fn, configs, hparams)

    estimator = tf.estimator.Estimator(model_fn=model_fn, config=run_config)

    return dict(
        estimator=estimator,
        train_input_fn=train_input_fn,
        eval_input_fn=eval_input_fn,
        train_steps=train_steps
    )

