import pandas as pd
import ftfy

# Define the file path
file_path = "all_data_with_users_hatespeech_0.csv"

# Read the CSV file with latin1 encoding
data = pd.read_csv(file_path, encoding='latin1')

# Function to clean and normalize text data using ftfy
def clean_text(text):
    if isinstance(text, str):
        # Use ftfy to fix text encoding issues
        text = ftfy.fix_text(text)
        # Normalize whitespace
        text = ' '.join(text.split())
    return text

# Apply the clean_text function to all string columns in the dataframe
data = data.applymap(clean_text)

# Save the dataframe to a new CSV file with utf-8 encoding
corrected_file_path = "corrected_all_data_with_users_hatespeech_0.csv"
data.to_csv(corrected_file_path, index=False, encoding='utf-8')

# Optionally, reload the file to verify encoding was corrected
corrected_data = pd.read_csv(corrected_file_path, encoding='utf-8')
print(corrected_data.head())
