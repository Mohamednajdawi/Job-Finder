import io
from typing import List, Tuple

import PyPDF2
import streamlit as st
from iso3166 import countries
from logic.langgraph_pipeline import run_job_application_pipeline

# Constants
PAGE_TITLE = "Job Application Assistant"
PAGE_ICON = "💼"
COUNTRY_LIST = [("", "Select a country")] + [
    (country.alpha2, country.name) for country in countries
]

# Custom CSS
CUSTOM_CSS = """
<style>
.main {
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
.stButton>button {
    width: 100%;
}
.job-card {
    background-color: #f0f2f6;
    border-radius: 10px;
    padding: 1rem;
    margin-bottom: 1rem;
}
.cv-data-card {
    background-color: #e6f3ff;
    border-radius: 10px;
    padding: 1rem;
    margin-bottom: 1rem;
}
.cv-data-card .streamlit-expanderHeader {
    font-weight: bold;
    color: #1e88e5;
}
</style>
"""


def extract_text_from_pdf(pdf_file: io.BytesIO) -> str:
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    return "".join(page.extract_text() for page in pdf_reader.pages)


def render_input_fields() -> Tuple[str, str, str, str, str]:
    col1, col2 = st.columns(2)

    with col1:
        applicant_name = st.text_input("👤 Applicant Name", placeholder="e.g., Mohammad Alnajdawi")
        job_title = st.text_input("🔍 Job Title", placeholder="e.g., Software Engineer")
        country = st.selectbox(
            "🌍 Country",
            options=[c[0] for c in COUNTRY_LIST],
            format_func=lambda x: dict(COUNTRY_LIST)[x],
            index=0,
        )

    with col2:
        skills = st.text_input("🛠️ Skills", placeholder="e.g., Python, JavaScript, React")
        education = st.text_input(
            "🎓 Education", placeholder="e.g., Bachelor's in Computer Science"
        )

    return applicant_name, job_title, country, skills, education


def render_job_opportunities(results: dict):
    st.subheader("📋 Job Opportunities")
    for i, (job, analysis, cover_letter) in enumerate(
        zip(results["jobs"], results["analyzed_jobs"], results["cover_letters"])
    ):
        with st.expander(f"{job['title']} at {job['company']}"):
            st.markdown(
                f"""
                <div class="job-card">
                    <h4>{job['title']}</h4>
                    <p><strong>Company:</strong> {job['company']}</p>
                    <p><strong>Link:</strong> <a href="{job['link']}" target="_blank">{job['link']}</a></p>
                    <h5>Job Analysis:</h5>
                    <p>{analysis["analysis"]}</p>
                    <h5>Generated Cover Letter:</h5>
                    <p>{cover_letter}</p>                        
                </div>
                """,
                unsafe_allow_html=True,
            )


def display_cv_data(cv_data: dict):
    st.markdown('<div class="cv-data-card"><h4>📄 CV Extracted Data</h4>', unsafe_allow_html=True)

    for section, content in cv_data.items():
        with st.expander(f"{section.capitalize()}"):
            if isinstance(content, list):
                for item in content:
                    st.markdown(f"• {item}")
            elif isinstance(content, dict):
                for key, value in content.items():
                    st.markdown(f"**{key}:** {value}")
            else:
                st.markdown(content)

    st.markdown("</div>", unsafe_allow_html=True)


def main():
    st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout="wide")
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    st.title("🚀 Job Application Assistant")
    st.write("Let's help you find and apply for your dream job!")

    applicant_name, job_title, country, skills, education = render_input_fields()

    uploaded_cv = st.file_uploader("📄 Upload CV", type=["pdf"])

    if st.button("Generate Job Applications", key="generate"):
        if (job_title and skills and education) or uploaded_cv:
            with st.spinner("🔄 Processing your request... This may take a moment."):
                cv_text = extract_text_from_pdf(uploaded_cv) if uploaded_cv else ""
                results = run_job_application_pipeline(
                    cv_text, applicant_name, job_title, country, skills, education
                )

            st.success("✅ Job opportunities found! Check them out below.")

            display_cv_data(results["cv_data_extract"])

            render_job_opportunities(results)
        else:
            st.error("⚠️ Please fill in all fields and upload your CV to generate job applications.")

    st.sidebar.title("About")
    st.sidebar.info(
        "This Job Application Assistant helps you find relevant job opportunities "
        "and generates customized cover letters based on your skills and experience."
    )


if __name__ == "__main__":
    main()
