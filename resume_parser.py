import io
import re
import spacy
import pandas as pd
import docx2txt
import PyPDF2
from pdfminer.high_level import extract_text
import nltk
from nltk.corpus import stopwords

# Download NLTK resources with better error handling
try:
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt', quiet=True)
    # Add punkt_tab as mentioned in the error message
    nltk.download('punkt_tab', quiet=True)
except Exception as e:
    print(f"Warning: NLTK resource download issue: {str(e)}")
    print("If parsing fails, manually download required resources with:")
    print("import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('punkt_tab')")

class ResumeParser:
    def __init__(self):
        # Load spaCy model
        try:
            self.nlp = spacy.load('en_core_web_sm')
        except:
            # If model not found, download it
            import subprocess
            subprocess.call([
                'python', '-m', 'spacy', 'download', 'en_core_web_sm'
            ])
            self.nlp = spacy.load('en_core_web_sm')
        
        # Make sure NLTK resources are available
        try:
            # Test if resources are available
            from nltk.tokenize import word_tokenize
            word_tokenize("Test sentence")
        except LookupError:
            print("Re-downloading NLTK resources...")
            nltk.download('punkt', quiet=False, force=True)
            nltk.download('punkt_tab', quiet=False, force=True)
            nltk.download('stopwords', quiet=False, force=True)
        
        # Common skills list (can be expanded)
        self.skills_db = [
            'python', 'java', 'c++', 'sql', 'javascript', 'react', 'angular',
            'node.js', 'html', 'css', 'aws', 'azure', 'gcp', 'docker', 'kubernetes',
            'machine learning', 'data science', 'ai', 'tensorflow', 'pytorch',
            'nlp', 'data analysis', 'statistics', 'excel', 'tableau', 'power bi',
            'git', 'ci/cd', 'agile', 'scrum', 'project management', 'communication'
        ]
    
    def parse_resume(self, resume_bytes, filename):
        """Parse resume file and extract information"""
        text = ""
        file_extension = filename.split('.')[-1].lower()
        
        # Extract text based on file type
        try:
            if file_extension == 'pdf':
                text = self._extract_text_from_pdf(io.BytesIO(resume_bytes))
            elif file_extension == 'docx':
                text = docx2txt.process(io.BytesIO(resume_bytes))
            else:
                return None
        except Exception as e:
            print(f"Error extracting text from {filename}: {str(e)}")
            return None
            
        # Process the text
        if text:
            return self._extract_information(text, filename)
        return None
    
    def _extract_text_from_pdf(self, pdf_file):
        """Extract text from PDF file using multiple methods for better results"""
        text = ""
        try:
            text = extract_text(pdf_file)
        except:
            try:
                # Fallback to PyPDF2
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            except:
                pass
        return text
    
    def _extract_information(self, text, filename):
        """Extract structured information from resume text"""
        doc = self.nlp(text)
        
        # Extract skills
        skills = self._extract_skills(text)
        
        # Extract education (simple pattern matching)
        education = self._extract_education(text)
        
        # Extract experience (simple approach)
        experience = self._extract_experience(text)
        
        return {
            'name': filename,
            'raw_text': text,
            'skills': skills,
            'education': education,
            'experience': experience
        }
    
    def _extract_skills(self, text):
        """Extract skills from text"""
        skills = []
        # Convert to lowercase and clean text
        text_lower = text.lower()
        
        # Look for skills in the text
        for skill in self.skills_db:
            if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
                skills.append(skill)
                
        return skills
    
    def _extract_education(self, text):
        """Extract education information"""
        education = []
        education_keywords = ['bachelor', 'master', 'phd', 'degree', 'university', 
                             'college', 'school', 'institute', 'diploma']
        
        sentences = nltk.sent_tokenize(text)
        for sentence in sentences:
            for keyword in education_keywords:
                if keyword.lower() in sentence.lower():
                    education.append(sentence.strip())
                    break
        
        return education
    
    def _extract_experience(self, text):
        """Extract work experience information"""
        experience = []
        exp_keywords = ['experience', 'work', 'employment', 'job', 'career', 
                       'position', 'role']
        
        sentences = nltk.sent_tokenize(text)
        for sentence in sentences:
            for keyword in exp_keywords:
                if keyword.lower() in sentence.lower():
                    experience.append(sentence.strip())
                    break
        
        return experience
