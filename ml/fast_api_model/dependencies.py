from keras_core.src.saving import load_model

folder_model = "../ml_core/model_weights/"

from pathlib import Path

model_name = "deepwoke_fasttext_nlp_all_data.csv_20240626-161852-model.keras"
file_path_model = Path(__file__).resolve().parent.parent / "ml_core" / "model_weights" / model_name
if not file_path_model.exists():
    raise ValueError(f"{file_path_model} cannot be opened for loading!")

print(file_path_model.absolute())

def predict_class(input_text):
    model = load_model(file_path_model)  # Define this function to load your model
    return model.predict(input_text)
