import fitz  # PyMuPDF for PDF text extraction
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Download necessary NLTK data
nltk.download("punkt")
nltk.download("stopwords")

# List of important keywords for the job (Example: Data Science job)
important_keywords = {
    "machine learning", "deep learning", "python", "data analysis", "statistics",
    "artificial intelligence", "NLP", "TensorFlow", "PyTorch", "SQL", "data visualization"
}

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    doc = fitz.open(pdf_path)
    text = " "
    for page in doc:
        text += page.get_text("text")
    return text.lower()

def extract_text_from_txt(txt_path):
    """Extract text from a TXT file."""
    with open(txt_path, "r", encoding="utf-8") as file:
        return file.read().lower()

def clean_text(text):
    """Clean and tokenize text, removing stopwords and punctuation."""
    tokens = word_tokenize(text)
    words = [word for word in tokens if word.isalnum()]
    filtered_words = [word for word in words if word not in stopwords.words("english")]
    return set(filtered_words)

def check_keywords(resume_text):
    """Compare extracted resume text with important keywords."""
    resume_words = clean_text(resume_text)
    found_keywords = resume_words.intersection(important_keywords)
    missing_keywords = important_keywords - found_keywords
    
    return found_keywords, missing_keywords

def main():
    file_path = input("Enter the path of your resume (PDF or TXT): ")
    
    if file_path.endswith(".pdf"):
        resume_text = extract_text_from_pdf(file_path)
    elif file_path.endswith(".txt"):
        resume_text = extract_text_from_txt(file_path)
    else:
        print("Unsupported file format. Please use PDF or TXT.")
        return
    
    found_keywords, missing_keywords = check_keywords(resume_text)
    
    print("\n✅ Keywords found in your resume:")
    print(", ".join(found_keywords))
    
    print("\n⚠️ Keywords missing from your resume:")
    print(", ".join(missing_keywords))
    
    if missing_keywords:
        print("\n✨ Tip: Add these missing keywords to improve your ATS score!")

if __name__ == "__main__":
    main()
