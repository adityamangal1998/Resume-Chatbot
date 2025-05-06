import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ResumeMatcher:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')
    
    def match_resumes_to_job(self, resume_docs, job_description):
        """Match resumes to job description and return ranked results"""
        # Extract job skills
        job_skills = self._extract_skills(job_description)
        
        # Prepare for TF-IDF
        documents = [job_description]
        for resume in resume_docs:
            documents.append(resume['raw_text'])
        
        # Calculate TF-IDF and similarity
        try:
            tfidf_matrix = self.vectorizer.fit_transform(documents)
            cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
            similarity_scores = cosine_similarities[0]
        except:
            # Fallback if TF-IDF fails (e.g., with very short texts)
            similarity_scores = np.zeros(len(resume_docs))
        
        # Calculate skill match scores
        results = []
        for i, resume in enumerate(resume_docs):
            resume_skills = set(resume['skills'])
            job_skills_set = set(job_skills)
            
            # Calculate skills overlap
            matching_skills = resume_skills.intersection(job_skills_set)
            skills_score = len(matching_skills) / max(1, len(job_skills_set))
            
            # Calculate combined score (TF-IDF similarity + skills match)
            combined_score = (0.4 * similarity_scores[i]) + (0.6 * skills_score)
            
            results.append((
                resume['name'], 
                combined_score,
                ', '.join(matching_skills) if matching_skills else "None"
            ))
        
        # Sort by score
        results.sort(key=lambda x: x[1], reverse=True)
        return results
    
    def _extract_skills(self, text):
        """Extract potential skills from job description"""
        # Common tech skills to look for
        common_skills = [
            'python', 'java', 'c++', 'sql', 'javascript', 'react', 'angular',
            'node.js', 'html', 'css', 'aws', 'azure', 'gcp', 'docker', 'kubernetes',
            'machine learning', 'data science', 'ai', 'tensorflow', 'pytorch',
            'nlp', 'data analysis', 'statistics', 'excel', 'tableau', 'power bi',
            'git', 'ci/cd', 'agile', 'scrum', 'project management', 'communication'
        ]
        
        found_skills = []
        text_lower = text.lower()
        
        # Look for skills in the text
        for skill in common_skills:
            if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
                found_skills.append(skill)
                
        return found_skills
