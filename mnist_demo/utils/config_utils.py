import tensorflow as tf

from google.protobuf import text_format

from mnist_demo.protos import pipeline_pb2

def get_configs_from_pipeline_file(pipeline_config_path, config_override=None):
    pipeline_config = pipeline_pb2.TrainEvalPipelineConfig()
    with tf.gfile.GFile(pipeline_config_path, 'r') as f:
        proto_str = f.read()
        text_format.Merge(proto_str, pipeline_config)

    if config_override is not None:
        text_format.Merge(config_override, pipeline_config)

    return create_configs_from_pipeline_proto(pipeline_config)

def create_configs_from_pipeline_proto(pipeline_config):
    configs = {}
    configs['train_config'] = pipeline_config.train_config
    configs['eval_config'] = pipeline_config.eval_config
    configs['train_input_config'] = pipeline_config.train_input_config
    configs['eval_input_config'] = pipeline_config.eval_input_config

    return configs