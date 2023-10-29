import pdfplumber
from docx import Document

class pdf_file():
    def __int__(self):
        pass
    def convert_to_text(self, uploaded_file):
        with pdfplumber.open(uploaded_file) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()

            return text

class docx_file():
    def __int__(self):
        pass
    def convert_to_text(self, uploaded_file):
        doc_file = Document(uploaded_file)
        text_string = ""
        for paragraph in doc_file.paragraphs:
            text_string += paragraph.text + '\n'
        return text_string

def run(uploaded_file):
    if type(uploaded_file) == str:
        method_str = f"{uploaded_file.split('.')[-1]}_file"
    else:
        method_str = f"{uploaded_file.name.split('.')[-1]}_file"
    class_str = globals()[method_str]
    converter_obj = class_str()
    text = converter_obj.convert_to_text(uploaded_file)
    return text


