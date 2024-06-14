from keras_core.src.saving import load_model

folder_model = "../ml_core/model_weights/"

from pathlib import Path

file_path_model = Path(__file__).resolve().parent.parent / "ml_core" / "model_weights" / "fasttext_nlp_20240613-131608-model.keras"
if not file_path_model.exists():
    raise ValueError(f"{file_path_model} cannot be opened for loading!")

print(file_path_model.absolute())

def predict_class(input_text):
    model = load_model(file_path_model)  # Define this function to load your model
    return model.predict(input_text)
