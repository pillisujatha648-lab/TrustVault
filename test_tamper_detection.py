
import os
from dotenv import load_dotenv

load_dotenv()

from app import create_app
from app.encryption import decrypt_file

app = create_app()

with app.app_context():

    storage_folder = app.config["PRIVATE_STORAGE"]

    files = [
        file for file in os.listdir(storage_folder)
        if file.endswith(".encrypted")
    ]

    filename = files[0]

    file_path = os.path.join(storage_folder, filename)

    with open(file_path, "rb") as f:
        encrypted_data = bytearray(f.read())

    # Change one byte in memory
    encrypted_data[-1] ^= 1

    try:
        decrypt_file(bytes(encrypted_data))
        print("WARNING: Tampering was not detected.")

    except Exception:
        print("SUCCESS: Tampering detected!")
        print("Modified encrypted data was rejected.")
