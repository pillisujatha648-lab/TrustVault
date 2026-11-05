
from pathlib import Path
from dotenv import load_dotenv
from app.encryption import encrypt_file, decrypt_file
from cryptography.exceptions import InvalidTag

load_dotenv()

folder = Path("private_storage")

for file in folder.glob("*.encrypted"):

    data = file.read_bytes()

    try:
        decrypt_file(data)
        print(file.name, "- Already encrypted. Skipped.")

    except InvalidTag:

        if data.startswith(b"%PDF-"):
            encrypted_data = encrypt_file(data)
            file.write_bytes(encrypted_data)
            print(file.name, "- Successfully encrypted.")

        else:
            print(file.name, "- Unknown format. Skipped.")

    except Exception as error:
        print(file.name, "- Error:", error)
