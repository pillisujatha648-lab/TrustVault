from dotenv import load_dotenv
from pathlib import Path
from app.encryption import decrypt_file
from cryptography.exceptions import InvalidTag

load_dotenv()

folder = Path("private_storage")

for file in folder.glob("*.encrypted"):

    try:
        decrypted_data = decrypt_file(file.read_bytes())

        print(file.name, "- ENCRYPTED AND VERIFIED")

    except InvalidTag:
        print(file.name, "- NOT VERIFIED")

    except Exception as e:
        print(file.name, "- ERROR:", e)
        