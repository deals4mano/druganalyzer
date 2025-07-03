import base64

def encode_pdf_to_base64(filepath):
    """
    Reads a PDF file from the given filepath and returns its content as a Base64-encoded string.

    :param filepath: Path to the PDF file
    :return: Base64-encoded string of the PDF content
    """
    print(f"Encoding PDF file: {filepath}")
    try:
        with open(filepath, "rb") as pdf_file:
            pdf_content = pdf_file.read()
            base64_encoded = base64.b64encode(pdf_content).decode("utf-8")
            return base64_encoded
    except FileNotFoundError:
        return "Error: File not found."
    except Exception as e:
        return f"Error: {str(e)}"
  
   
if __name__ == "__main__":
    # Example usage
    pdf_path = "E:/Projects/aidrugalayzer/test/MRN123456-PatientChart1.pdf"  # Replace with your PDF file path
    encoded_pdf = encode_pdf_to_base64(pdf_path)
    print(encoded_pdf)  # Output the Base64-encoded string