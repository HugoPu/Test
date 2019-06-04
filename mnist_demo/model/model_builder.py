from mnist_demo.model.model_architectures import FullConnect

def build(model_config, is_training, add_summaries=True):
    return _build_cnn_model(model_config, is_training, add_summaries)

def _build_cnn_model(model_config, is_training, add_summaries):
    return FullConnect(model_config, is_training, add_summaries)