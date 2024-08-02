import streamlit as st
from iso3166 import countries
from logic.langgraph_pipeline import run_job_application_pipeline


def main():
    st.set_page_config(page_title="Job Application Assistant", page_icon="💼", layout="wide")

    # Custom CSS
    st.markdown(
        """
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
        </style>
    """,
        unsafe_allow_html=True,
    )

    st.title("🚀 Job Application Assistant")
    st.write("Let's help you find and apply for your dream job!")
    country_list = [("", "Select a country")] + [
        (country.alpha2, country.name) for country in countries
    ]

    col1, col2 = st.columns(2)

    with col1:
        applicant_name = st.text_input("👤 Applicant Name", placeholder="e.g., Mohammad Alnajdawi")
        job_title = st.text_input("🔍 Job Title", placeholder="e.g., Software Engineer")
        country = st.selectbox(
            "🌍 Country",
            options=[c[0] for c in country_list],
            format_func=lambda x: dict(country_list)[x],
            index=0,
        )

    with col2:
        skills = st.text_input("🛠️ Skills", placeholder="e.g., Python, JavaScript, React")
        education = st.text_input(
            "🎓 Education", placeholder="e.g., Bachelor's in Computer Science"
        )

    if st.button("Generate Job Applications", key="generate"):
        if job_title and skills and education:
            with st.spinner("🔄 Processing your request... This may take a moment."):
                results = run_job_application_pipeline(
                    applicant_name, job_title, country, skills, education
                )

            st.success("✅ Job opportunities found! Check them out below.")

            st.subheader("📋 Job Opportunities")
            for i, job in enumerate(results["jobs"]):
                with st.expander(f"{job['title']} at {job['company']}"):
                    st.markdown(
                        f"""
                    <div class="job-card">
                        <h4>{job['title']}</h4>
                        <p><strong>Company:</strong> {job['company']}</p>
                        <p><strong>Link:</strong> <a href="{job['link']}" target="_blank">{job['link']}</a></p>
                        <h5>Job Analysis:</h5>
                        <p>{results['analyzed_jobs'][i]["analysis"]}</p>
                        <h5>Generated Cover Letter:</h5>
                        <p>{results['cover_letters'][i]}</p>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )
        else:
            st.error("⚠️ Please fill in all fields to generate job applications.")

    st.sidebar.title("About")
    st.sidebar.info(
        "This Job Application Assistant helps you find relevant job opportunities "
        "and generates customized cover letters based on your skills and experience."
    )


if __name__ == "__main__":
    main()
