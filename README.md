# Resume Matching Application

A Streamlit application that extracts information from resumes and matches them against job descriptions using NLP techniques without relying on LLMs.

## Features

- Upload and parse multiple resumes (PDF, DOCX)
- Extract key information like skills, education, and experience
- Match resumes against job descriptions
- Rank candidates based on match scores
- View detailed candidate information

## Installation

1. Clone the repository
2. Install the required packages:
```bash
pip install -r requirements.txt
```
3. Download required language models:
```bash
python -m spacy download en_core_web_sm
python -m nltk.downloader punkt stopwords punkt_tab
```

## Usage

1. Run the application:
```bash
streamlit run app.py
```
2. Navigate to the URL displayed in the terminal (typically http://localhost:8501)
3. Upload resume files (PDF or DOCX format)
4. Enter a job description in the text area
5. Click "Match Resumes" to see the ranked results

## File Structure

- `app.py`: Main Streamlit application
- `resume_parser.py`: Resume parsing functionality
- `matcher.py`: Resume-job description matching logic 
- `requirements.txt`: Required dependencies

## Dependencies

- streamlit
- pandas
- spacy
- scikit-learn
- PyPDF2
- pdfminer.six
- docx2txt
- nltk

## Troubleshooting

### NLTK Resource Issues

If you encounter NLTK resource errors, manually download the required packages:
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt_tab')
```

### PDF Parsing Issues

If PDF parsing fails:
1. Ensure you have all dependencies installed
2. Try converting the PDF to text using another tool first
3. Check if the PDF contains actual text rather than just images

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
