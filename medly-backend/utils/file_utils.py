import os

def save_uploaded_file(file, file_id):
    os.makedirs("uploads", exist_ok=True)
    file_path = f"uploads/{file_id}.pdf"
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    return file_path