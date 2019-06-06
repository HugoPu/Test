from mnist_demo.model.model_architectures import FullConnect
from mnist_demo.protos import model_pb2

def build(model_config, is_training, add_summaries=True):
    if not isinstance(model_config, model_pb2.Model):
        raise ValueError()
    architecture = model_config.WhichOneof('model')
    if architecture == 'dense':
        return _build_cnn_model(model_config.dense, is_training, add_summaries)
    else:
        raise ValueError()

def _build_cnn_model(model_config, is_training, add_summaries):
    return FullConnect(model_config, is_training, add_summaries)