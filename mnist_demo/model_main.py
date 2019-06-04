import  tensorflow as tf

from mnist_demo.utils import model_utils
from mnist_demo.model import model_hparams

flags = tf.flags

flags.DEFINE_string('model_dir', '', 'Path to output model dictory')
flags.DEFINE_string('pipeline_config_path', '', 'Path to pipeline file.')
flags.DEFINE_integer('num_train_steps', None, 'Number of train steps.')
flags.DEFINE_string(
    'hparams_overrides', None, 'Hyperparameter overrides, '
    'represented as a string containing comma-separated '
    'hparam_name=value pairs.')
flags.DEFINE_string('checkpoint_dir', None, 'Path to directory holding a checkpoint. If `checkpoint_dir` '
                                            'is provided. this binary operates in eval-only mode, writing'
                                            'resulting metrics to `model_dir')
flags.DEFINE_string('run_once', False, 'IF running in eval-only mode, whether to run just one round'
                                       'of eval vs running continuously (default)')

FLAGS = flags.FLAGS

def main(argv):
    flags.mark_flag_as_required('model_dir')
    flags.mark_flag_as_required('pipeline_config_path')
    config = tf.estimator.RunConfig(model_dir=FLAGS.model_dir)

    train_and_eval_dict = model_utils.create_estimator_and_inputs(
        run_config=config,
        hparams=model_hparams.create_hparams(FLAGS.hparams_overrides),
        pipeline_config_path=FLAGS.pipeline_config_path,
        train_steps=FLAGS.num_train_steps
    )


if __name__ == '__main__':
    tf.app.run()