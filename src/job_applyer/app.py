import streamlit as st
from logic.langgraph_pipeline import run_job_application_pipeline
from ui.components import display_cv_data, render_input_fields, render_job_opportunities
from ui.styles import CUSTOM_CSS
from utils.pdf_extractor import extract_text_from_pdf

# Constants
PAGE_TITLE = "Job Application Assistant"
PAGE_ICON = "💼"


def main():
    st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout="wide")
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    # Initialize session state
    if "cv_data" not in st.session_state:
        st.session_state.cv_data = None
    if "job_results" not in st.session_state:
        st.session_state.job_results = None
    if "page" not in st.session_state:
        st.session_state.page = "home"

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "CV Data"])

    if page == "Home":
        show_home_page()
    elif page == "CV Data":
        show_cv_data_page()

    st.sidebar.title("About")
    st.sidebar.info(
        "This Job Application Assistant helps you find relevant job opportunities "
        "and generates customized cover letters based on your skills and experience."
    )


def show_home_page():
    st.title("🚀 Job Application Assistant")
    st.write("Let's help you find and apply for your dream job!")

    applicant_name, job_title, country, skills, education, number_of_jobs = render_input_fields()

    uploaded_cv = st.file_uploader("📄 Upload CV", type=["pdf"])

    if st.button("Generate Job Applications", key="generate"):
        if (applicant_name and job_title and skills and education) or uploaded_cv:
            with st.spinner("🔄 Processing your request... This may take a moment."):
                cv_text = extract_text_from_pdf(uploaded_cv) if uploaded_cv else ""
                results = run_job_application_pipeline(
                    cv_text, applicant_name, job_title, country, skills, education, number_of_jobs
                )

            st.success("✅ Job opportunities found! Check them out below.")

            # Store results in session state
            st.session_state.cv_data = results["cv_data_extract"]
            st.session_state.job_results = results

            render_job_opportunities(results)

        else:
            st.error("⚠️ Please fill in all fields and upload your CV to generate job applications.")

    # Display cached job results if available
    elif st.session_state.job_results:
        st.success("✅ Showing previously generated job opportunities.")
        render_job_opportunities(st.session_state.job_results)


def show_cv_data_page():
    st.title("📄 CV Data")
    if st.session_state.cv_data:
        display_cv_data(st.session_state.cv_data)
    else:
        st.warning("No CV data available. Please generate job applications first.")


if __name__ == "__main__":
    main()
