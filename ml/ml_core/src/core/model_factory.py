from ml.ml_core.src.core.mlp_builder import mlp_builder
from ml.ml_core.src.core.convnet_builder import convnet_builder


def model_factory(model_name, input_dim, output_dim):
    if model_name == 'mlp':
        return mlp_builder(input_dim, output_dim)
    if model_name == 'convnet':
        return convnet_builder(input_dim, output_dim)
