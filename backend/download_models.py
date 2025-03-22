import os
import zipfile
import gdown

def download_and_extract_models():
    zip_path = "models.zip"
    models_dir = "models"

    # Check if models directory already exists
    if os.path.exists(models_dir):
        print("Models directory exists, skipping download.")
        return

    # File ID from your Google Drive share link
    file_id = "1oJ3V8Bz4YWldLCbFt_g_i1eB4izQ3cQF"  
    url = f"https://drive.google.com/uc?id={file_id}"
    
    # Download the ZIP file if it doesn't exist
    if not os.path.exists(zip_path):
        print("Downloading models.zip from Google Drive...")
        gdown.download(url, zip_path, quiet=False)
    
    # Extract the ZIP file
    print("Extracting models.zip...")
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(".")
    
    # Optionally, remove the ZIP file after extraction
    os.remove(zip_path)
    print("Models downloaded and extracted successfully!")

if __name__ == "__main__":
    download_and_extract_models()
