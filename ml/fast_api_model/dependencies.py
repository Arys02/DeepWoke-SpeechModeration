from keras_core.src.saving import load_model

folder_model = "../ml_core/model_weights/"


def predict_class(input_text):
    model = load_model(
        f"{folder_model}fasttext_nlp_20240613-131608-model.keras")  # Define this function to load your model
    return model.predict(input_text)
