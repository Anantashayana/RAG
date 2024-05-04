import streamlit as st
import docx
import os
import rag
from myPdfReader import PdfOcrCorpus


# Function to save uploaded file
def save_uploaded_file(uploaded_file):
    file_path = os.path.join(os.getcwd(), uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

# Function to extract text from PDF files
def extract_text_from_pdf(file):
    path = save_uploaded_file(file)
    pdf = PdfOcrCorpus()
    text = pdf.simplePdftoText(path)
    return text

# Function to extract text from DOCX files
def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = ""
    for para in doc.paragraphs:
        text += para.text
    return text

# Function to upload file and return text
def upload_file_and_get_text(file):
    text = ""
    file_type = file.type.split('/')[1]
    print(file_type)
    if file_type == "pdf":
        text = extract_text_from_pdf(file)
    elif file_type == "vnd.openxmlformats-officedocument.wordprocessingml.document":
        text = extract_text_from_docx(file)
    return text

# Streamlit UI
def main():
    st.title("Document Query System")

    # Upload file
    uploaded_file = st.file_uploader("Upload PDF or DOCX file", type=['pdf', 'docx'])
    if uploaded_file is not None:
        st.write("File Uploaded Successfully!")

        # Convert file to text
        text = upload_file_and_get_text(uploaded_file)

        # Save text to a temporary file
        temp_file_path = "temp_file.txt"
        with open(temp_file_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Text Extracted:{text}")
        rag.insertData(temp_file_path)
        # Query document
        query = st.text_input("Enter your query:")
        if st.button("Search"):
            result = rag.queryDB2(query)
            st.write(result)

            # Delete temporary file
            os.remove(temp_file_path)

    # Or paste text
    st.header("Or paste text")
    text_input = st.text_area("Paste your text here:")
    # Save text to a temporary file

    if st.button("Submit"):
        temp_file_path = "temp_file.txt"
        with open(temp_file_path, "w", encoding="utf-8") as f:
            f.write(text_input)
        rag.insertData(temp_file_path)
        query = st.text_input("Enter your query:")
        if st.button("Search"):
            result = rag.queryDB2(query)
            st.write(result)

            # Delete temporary file
            os.remove(temp_file_path)

# Run the app
if __name__ == "__main__":
    main()
