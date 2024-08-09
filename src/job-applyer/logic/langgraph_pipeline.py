from typing import Any, Dict, List

from logic.cover_letter_gen import generate_cover_letter
from logic.cv_extractor import cv_data_extract
from logic.job_analyzer import analyze_job_description
from logic.job_extractor import job_description_data_extract
from logic.linkedin_job_scraper import search_linkedin_jobs

# from logic.linkedin_data_scraper import search_linkedin_data


def run_job_application_pipeline(
    cv_text, applicant_name, job_title, country, user_skills, user_education, number_of_jobs
):
    # Step 1: Search for jobs
    def search_jobs(job_title, country, number_of_jobs):
        return search_linkedin_jobs(job_title, country, number_of_jobs)

    # Step 2: Analyze jobs
    def analyze_jobs(jobs, cv_text):
        analyzed_jobs = []
        for job in jobs:
            analysis = analyze_job_description(
                job["description"], user_skills, user_education, cv_text
            )
            job_extracted_data = job_description_data_extract(job["description"])
            analyzed_jobs.append(
                {**job, "analysis": analysis, "job_extracted_data": job_extracted_data}
            )
        return analyzed_jobs

    # Step 3: Generate cover letter
    def generate_cover_letters(
        cv_text: str,
        applicant_name: str,
        analyzed_jobs: List[Dict[str, Any]],
        user_skills: List[str],
        user_education: str,
    ) -> Dict[str, str]:
        cover_letters = []
        for job in analyzed_jobs:
            cover_letter = generate_cover_letter(
                cv_text,
                applicant_name,
                job["title"],
                job["company"],
                job["description"],
                job["analysis"]["cv_summary"],
                user_skills,
                user_education,
            )
            cover_letters.append(cover_letter)
        return cover_letters

    # Run the pipeline
    print("------------")
    print("Pipeline Started ...")
    cv_data = cv_data_extract(cv_text)
    print("CV data has been extracted")
    jobs = search_jobs(job_title, country, number_of_jobs)
    print("Jobs Founded")
    analyzed_jobs = analyze_jobs(jobs, cv_text)
    print("Jobs Analyzed")
    cover_letters = generate_cover_letters(
        cv_text, applicant_name, analyzed_jobs, user_skills, user_education
    )
    print("Cover Letter Has been Generated")
    print("------------")

    return {
        "jobs": jobs,
        "cv_data_extract": cv_data,
        "analyzed_jobs": analyzed_jobs,
        "cover_letters": cover_letters,
    }
