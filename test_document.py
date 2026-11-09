
from pathlib import Path
from src.document_processor import extract_document_text

# Enter the path of your test document
file_path = Path("documents/sample.pdf")

# Read the document
with file_path.open("rb") as file:
    file_bytes = file.read()


class UploadedFile:
    """A simple object for testing document extraction."""

    def __init__(self, name, data):
        self.name = name
        self.data = data

    def getvalue(self):
        return self.data


uploaded_file = UploadedFile(
    file_path.name,
    file_bytes
)

try:
    extracted_text = extract_document_text(uploaded_file)

    print("\nDocument extracted successfully!")
    print("\nExtracted content:\n")
    print(extracted_text[:5000])

except Exception as error:
    print("Error:", error)
