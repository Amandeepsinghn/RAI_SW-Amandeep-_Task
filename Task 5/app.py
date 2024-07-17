import streamlit as st
from PyPDF2 import PdfReader
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
import nltk 
from nltk.stem import PorterStemmer
import tensorflow as tf 
from tensorflow.keras.preprocessing.text import Tokenizer
from nltk.corpus import stopwords
import re 
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB, GaussianNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from tensorflow.keras.utils import pad_sequences
import fitz  # PyMuPDF

# Load tokenizer and model
tokenizer = PegasusTokenizer.from_pretrained("google/pegasus-xsum")
model = PegasusForConditionalGeneration.from_pretrained("google/pegasus-xsum")

# Function to extract text from PDF
def get_pdf_text(pdf_path):
    pdf_doc = fitz.open(pdf_path)
    text = ""
    for page in pdf_doc:
        text += page.get_text()
    return text

# Streamlit app
def main():
    st.title("PDF Summarizer using Pegasus")
    
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file is not None:
        with st.spinner("Extracting text from PDF..."):
            text = get_pdf_text(uploaded_file)
        
        st.write("Extracted Text:")
        st.write(text)
        
        ps = PorterStemmer()
        text = re.sub(r"[^a-zA-Z]", " ", text)
        text = text.lower()
        text = text.split()
        text = " ".join(text)
        
        tokens = tokenizer(text, truncation=True, padding="longest", return_tensors="pt", max_length=500)
        
        with st.spinner("Generating summary..."):
            summary = model.generate(**tokens)
            summary_text = tokenizer.decode(summary[0], skip_special_tokens=True)
        
        st.write("Summary:")
        st.write(summary_text)

if __name__ == "__main__":
    main()
