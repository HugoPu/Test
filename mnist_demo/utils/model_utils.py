import os
import tensorflow as tf
import copy
import functools

from mnist_demo.utils.config_utils import get_configs_from_pipeline_file
from mnist_demo.utils import eval_utils
from mnist_demo.model.model_builder import build
from mnist_demo.inputs import create_eval_input_fn, create_predict_input_fn, create_train_input_fn

def create_model_fn(init_model_fn, configs, hparams):
    train_config = configs['train_config']
    eval_config = configs['eval_config']

    def model_fn(features, labels, mode, params=None):
        params = params or {}
        is_training = mode == tf.estimator.ModeKeys.TRAIN
        model = init_model_fn(is_training=is_training)

        predictions = model.predict(features['image'])
        # predictions = tf.keras.layers.Dense(10)(features['image'])

        format_predictions = None
        if mode in (tf.estimator.ModeKeys.PREDICT, tf.estimator.ModeKeys.EVAL):
            format_predictions = model.format_output(predictions)

        loss = None
        if mode in (tf.estimator.ModeKeys.TRAIN, tf.estimator.ModeKeys.EVAL):
            loss = model.loss(predictions, labels)
            global_step = tf.train.get_or_create_global_step()

        train_op = None
        if mode == tf.estimator.ModeKeys.TRAIN:
            # loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=predictions, labels=labels))
            optimizer = tf.train.GradientDescentOptimizer(learning_rate=train_config.lr)
            train_op = optimizer.minimize(loss, global_step=global_step)
            # train_op = tf.contrib.layers.optimize_loss(
            #     loss=loss,
            #     global_step=global_step,
            #     learning_rate=train_config.lr,
            #     optimizer='Adam'
            # )

        eval_metric_ops = None
        if mode == tf.estimator.ModeKeys.EVAL:
            eval_metric_ops = eval_utils.get_eval_metrics_ops_for_evaluatiors(
                eval_config, format_predictions, labels)

        return tf.estimator.EstimatorSpec(
            mode=mode,
            predictions=format_predictions,
            loss=loss,
            train_op=train_op,
            eval_metric_ops=eval_metric_ops
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
    model_config = configs['model']
    train_config = configs['train_config']
    eval_config = configs['eval_config']
    train_input_config = configs['train_input_config']
    eval_input_config = configs['eval_input_config']
    eval_on_train_config = copy.deepcopy(train_input_config)

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

    eval_on_train_input_fn = create_eval_input_fn(
        eval_config=eval_config,
        eval_input_config=eval_on_train_config
    )

    predict_input_fn = create_predict_input_fn(None, None)

    model_fn = model_fn_creator(model_fn, configs, hparams)

    estimator = tf.estimator.Estimator(model_fn=model_fn, config=run_config)

    return dict(
        estimator=estimator,
        train_input_fn=train_input_fn,
        eval_input_fn=eval_input_fn,
        train_steps=train_steps,
        eval_on_train_input_fn=eval_on_train_input_fn,
        predict_input_fn=predict_input_fn
    )

def create_train_and_eval_specs(train_input_fn,
                                eval_input_fn,
                                eval_on_train_input_fn,
                                predict_input_fn,
                                train_steps,
                                eval_on_train_data=False,
                                final_exporter_name='Servo',
                                eval_spec_names=None):

    train_spec = tf.estimator.TrainSpec(
        input_fn=train_input_fn, max_steps=train_steps)
    exporter_name = final_exporter_name
    exporter = tf.estimator.FinalExporter(
        name=exporter_name, serving_input_receiver_fn=predict_input_fn)
    eval_spec = tf.estimator.EvalSpec(
        name='eval', input_fn=eval_input_fn, steps=None, exporters=None, throttle_secs=0)
    if eval_on_train_data:
        eval_spec = tf.estimator.EvalSpec(
            name='eval_on_train',input_fn=eval_on_train_input_fn, steps=None)

    return train_spec, eval_spec

def continuous_eval(estimator, model_dir, input_fn, train_steps, name):
    def terminate_eval():
        tf.logging.info('Terminating eval after 180 seconds of no checkpoints')
        return True

    for ckpt in tf.contrib.training.checkpoints_iterator(
        model_dir, min_interval_secs=180, timeout=None, timeout_fn=terminate_eval):

        tf.logging.info('Starting Evaluation.')

        try:
            eval_results = estimator.evaluate(
                input_fn=input_fn, steps=None, checkpoint_path=ckpt, name=name)
            tf.logging.info('Eval results:%s' % eval_results)

            # Terminate eval job when final checkpoint is reached
            current_step = int(os.path.basename(ckpt).split('-')[1])
            if current_step >= train_steps:
                tf.logging.info('Evaluation finished after training step %d' % current_step)
                break

        except tf.errors.NotFoundError:
            tf.logging.info('Checkpoint %s no longer exists, skipping checkpoint' % ckpt)
