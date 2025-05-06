import streamlit as st
import pandas as pd
import os
import io
from resume_parser import ResumeParser
from matcher import ResumeMatcher

st.set_page_config(page_title="Resume Matcher", layout="wide")

def main():
    st.title("Resume Matching System")
    
    st.sidebar.header("Upload Files")
    uploaded_resumes = st.sidebar.file_uploader(
        "Upload Resumes (PDF or DOCX)", 
        type=["pdf", "docx"], 
        accept_multiple_files=True
    )
    
    job_description = st.sidebar.text_area("Enter Job Description", height=300)
    
    if st.sidebar.button("Match Resumes") and uploaded_resumes and job_description:
        with st.spinner("Processing resumes..."):
            # Process resumes
            resume_docs = []
            for resume in uploaded_resumes:
                # Save the resume to a temp file
                bytes_data = resume.read()
                resume_name = resume.name
                parser = ResumeParser()
                parsed_resume = parser.parse_resume(bytes_data, resume_name)
                if parsed_resume:
                    resume_docs.append(parsed_resume)
            
            # Match resumes with job description
            if resume_docs:
                matcher = ResumeMatcher()
                matches = matcher.match_resumes_to_job(resume_docs, job_description)
                
                # Display results
                st.header("Matching Results")
                
                # Create a DataFrame for better display
                results_df = pd.DataFrame(matches, columns=["Resume", "Match Score", "Skills Matched"])
                results_df = results_df.sort_values(by="Match Score", ascending=False)
                
                # Display as a table
                st.dataframe(results_df)
                
                # Display detailed view for top matches
                st.header("Top Matches Details")
                for i, match in enumerate(matches[:3]):
                    with st.expander(f"Resume: {match[0]} (Score: {match[1]:.2f})"):
                        resume_idx = [doc['name'] for doc in resume_docs].index(match[0])
                        st.write("**Skills:**", ', '.join(resume_docs[resume_idx]['skills']))
                        st.write("**Experience:**", resume_docs[resume_idx]['experience'])
                        st.write("**Education:**", resume_docs[resume_idx]['education'])
            else:
                st.error("Failed to process any resumes!")
    
    # Instructions when no files are uploaded
    if not uploaded_resumes:
        st.info("Please upload resume files to get started.")
    
if __name__ == "__main__":
    main()
