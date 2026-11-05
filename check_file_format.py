from pathlib import Path

folder = Path("private_storage")

for file in folder.glob("*.encrypted"):

    data = file.read_bytes()

    print("\nFile:", file.name)
    print("Size:", len(data), "bytes")

    if data.startswith(b"%PDF-"):
        print("Format: Original PDF (not encrypted)")
    else:
        print("Format: Not a plain PDF - needs verification")