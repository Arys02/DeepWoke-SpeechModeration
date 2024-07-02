from ml.ml_core.src.model.mlp_builder import mlp_builder


def model_factory(model_name, input_dim, output_dim):
    if model_name == 'mlp':
        return mlp_builder(input_dim, output_dim)