import tensorflow as tf

from mnist_demo.utils import model_utils, log_uitls
from mnist_demo.model import model_hparams

flags = tf.flags

tf.logging.set_verbosity(tf.logging.INFO)

flags.DEFINE_string('model_dir', '/sdb/hugo/PythonWorkspace/Test/mnist_demo/output', 'Path to output model dictory')
flags.DEFINE_string('pipeline_config_path', '/sdb/hugo/PythonWorkspace/Test/mnist_demo/hparams/pipeline.config', 'Path to pipeline file.')
flags.DEFINE_integer('num_train_steps', 10000, 'Number of train steps.')
flags.DEFINE_boolean(
    'hparams_overrides', False, 'Hyperparameter overrides, '
    'represented as a string containing comma-separated '
    'hparam_name=value pairs.')
flags.DEFINE_integer('eval_interval', 500, 'Number of steps between each evaluation')
flags.DEFINE_string('checkpoint_dir', '/sdb/hugo/PythonWorkspace/Test/mnist_demo/output', 'Path to directory holding a checkpoint. If `checkpoint_dir` '
                                            'is provided. this binary operates in eval-only mode, writing'
                                            'resulting metrics to `model_dir')
flags.DEFINE_boolean('eval_training_data', False, '')
flags.DEFINE_boolean('run_once', False, 'IF running in eval-only mode, whether to run just one round'
                                       'of eval vs running continuously (default)')

FLAGS = flags.FLAGS

def main(argv):
    flags.mark_flag_as_required('model_dir')
    flags.mark_flag_as_required('pipeline_config_path')
    config = tf.estimator.RunConfig(model_dir=FLAGS.model_dir, save_checkpoints_steps=FLAGS.eval_interval)
    log_uitls.create_logger(model_dir=FLAGS.model_dir)

    train_and_eval_dict = model_utils.create_estimator_and_inputs(
        run_config=config,
        hparams=model_hparams.create_hparams(FLAGS.hparams_overrides),
        pipeline_config_path=FLAGS.pipeline_config_path,
        train_steps=FLAGS.num_train_steps
    )
    estimator = train_and_eval_dict['estimator']
    train_input_fn = train_and_eval_dict['train_input_fn']
    eval_input_fn = train_and_eval_dict['eval_input_fn']
    eval_on_train_input_fn = train_and_eval_dict['eval_on_train_input_fn']
    predict_input_fn = train_and_eval_dict['predict_input_fn']
    train_stpes = train_and_eval_dict['train_steps']

    if FLAGS.checkpoint_dir:
        if FLAGS.eval_training_data:
            name = 'training_data'
            input_fn = eval_on_train_input_fn
        else:
            name = 'validation_data'
            input_fn = eval_input_fn
        if FLAGS.run_once:
            estimator.evaluate(input_fn,
                               steps=None,
                               checkpoint_path=tf.train.latest_checkpoint(
                                   FLAGS.checkpoint_dir))
        else:
            model_utils.continuous_eval(estimator, FLAGS.checkpoint_dir, input_fn,
                                        train_stpes, name)
    else:
        train_spec, eval_spec = model_utils.create_train_and_eval_specs(
            train_input_fn,
            eval_input_fn,
            eval_on_train_input_fn,
            predict_input_fn,
            train_stpes,
            eval_on_train_data=False
        )
        tf.estimator.train_and_evaluate(estimator, train_spec, eval_spec)


if __name__ == '__main__':
    tf.app.run()