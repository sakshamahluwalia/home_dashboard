import re
from PyPDF2 import PdfReader

def parse_pdf(file_path):
    text_content = ''
    with open(file_path, 'rb') as file:
        reader = PdfReader(file)
        
        if reader.is_encrypted:
            try:
                # Attempt to decrypt with an empty password
                result = reader.decrypt('')
                if result == 1:
                    print("PDF decrypted with empty password.")
                else:
                    print("Failed to decrypt PDF with empty password.")
                    return None
            except Exception as e:
                print("Exception during decryption.")
                print(e)
                return None
        
        for page in reader.pages:
            text_content += page.extract_text()
    text_content = normalize_text(text_content)
    return text_content

def normalize_text(text):
    # Remove unnecessary newlines, spaces, and character breaks
    # Replace multiple line breaks and extra spaces with single spaces
    text = re.sub(r'\s+', ' ', text)  # Normalize spaces and newlines
    return text



