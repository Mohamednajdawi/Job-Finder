from typing import List, Tuple

import streamlit as st
from iso3166 import countries

# Constants
COUNTRY_LIST = [("", "Select a country")] + [
    (country.alpha2, country.name) for country in countries
]


def render_input_fields() -> Tuple[str, str, str, str, str, int]:
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
        number_of_jobs = st.number_input(
            "#️⃣ Number of jobs",
            value=1,
            min_value=1,
            max_value=5,
            placeholder="e.g., 1, 2, 3, ...",
            step=1,
        )
        skills = st.text_input("🛠️ Skills", placeholder="e.g., Python, JavaScript, React, ...")
        education = st.text_input(
            "🎓 Education", placeholder="e.g., Bachelor's in Computer Science"
        )

    return applicant_name, job_title, country, skills, education, number_of_jobs


def render_job_opportunities(results: dict):
    st.subheader("📋 Job Opportunities")
    for i, (job, analysis, cover_letter) in enumerate(
        zip(results["jobs"], results["analyzed_jobs"], results["cover_letters"])
    ):
        with st.expander(f"💼 {job['title']} at {job['company']}"):
            st.markdown(
                f"""
                <div class="job-card">
                    <h3><a href="{job['link']}" target="_blank" class="job-link">{job['title']}</a></h3>
                    <h4>🏢 {job['company']}</h4>
                </div>
                """,
                unsafe_allow_html=True,
            )

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### 📊 Job Details")
                job_data = analysis["job_extracted_data"]

                if job["location"]:
                    st.markdown(f"📍 **Location:** {job['location']}")

                if job["post_time"]:
                    st.markdown(f"🔔 **Was Posted:** {job['post_time']}")

                if job["applicants"]:
                    st.markdown(f"👤 **Number of Applicants:** {job['applicants']}")

                if job_data["salary"]:
                    st.markdown(f"💰 **Salary:** {job_data['salary']}")

                if job_data["applying_method"]:
                    st.markdown(f"📝 **How to Apply:** {job_data['applying_method'].value}")

                if job_data["remote_work_compatibility"]:
                    st.markdown(
                        f"🏠 **Remote Work:** {job_data['remote_work_compatibility'].value}"
                    )

                if job_data["additional_benefits"]:
                    st.markdown("🎁 **Additional Benefits:**")
                    for benefit in job_data["additional_benefits"]:
                        st.markdown(f"  • {benefit}")

            with col2:
                st.markdown("### 🎯 Match Analysis")
                match_percentage = analysis["analysis"]["match_percentage"]
                st.markdown(
                    f"<div class='match-percentage'>{match_percentage}% Match</div>",
                    unsafe_allow_html=True,
                )
                st.markdown("### 🎓 Education Alignment")
                st.markdown(
                    f"<div class='match-percentage'>{analysis['analysis']['education_alignment'].value}</div>",
                    unsafe_allow_html=True,
                )

                st.markdown("#### 🔍 Matching Skills")
                for skill in analysis["analysis"]["matching_skills"]:
                    st.markdown(
                        f"<span class='matching-skill'>✅ {skill}</span>", unsafe_allow_html=True
                    )

                st.markdown("#### 📚 Skills to Develop")
                for skill in analysis["analysis"]["skills_to_develop"]:
                    st.markdown(
                        f"<span class='skill-to-develop'>📖 {skill}</span>", unsafe_allow_html=True
                    )
            st.divider()
            st.markdown("### 📝 CV Summary")
            st.markdown(analysis["analysis"]["cv_summary"])
            st.divider()
            st.markdown("### 📄 Generated Cover Letter")
            st.markdown(cover_letter)


def display_cv_data(cv_data: dict):
    st.markdown('<div class="cv-data-card">', unsafe_allow_html=True)

    # Display personal information
    if "meta_data" in cv_data:
        st.markdown("### Personal Information")
        name = cv_data["meta_data"].get("name", "N/A")
        st.markdown(f"**Name:** {name}")

        contact_info = cv_data["meta_data"].get("contact_information", {})
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Location:** {contact_info.get('location', 'N/A')}")
            st.markdown(f"**Phone:** {contact_info.get('phone_number', 'N/A')}")
        with col2:
            st.markdown(f"**Email:** {contact_info.get('email', 'N/A')}")
            linkedin = contact_info.get("linkedin", "N/A")
            st.markdown(
                f"**LinkedIn:** [{linkedin}]({linkedin})"
                if linkedin != "N/A"
                else f"**LinkedIn:** {linkedin}"
            )

    # Display summary
    if "summary" in cv_data:
        st.markdown("### Summary")
        st.markdown(cv_data["summary"])

    # Display education (hidden by default)
    if "education" in cv_data:
        with st.expander("### Education", expanded=False):
            for edu in cv_data["education"]:
                st.markdown(f"**{edu.get('degree', 'Degree')} in {edu.get('major', 'Major')}**")
                st.markdown(
                    f"{edu.get('institution', 'Institution')} | {edu.get('dates', 'Dates')}"
                )
                st.markdown("---")

    # Display experience (hidden by default)
    if "experience" in cv_data:
        with st.expander("### Work Experience", expanded=False):
            for exp in cv_data["experience"]:
                st.markdown(
                    f"**{exp.get('job_title', 'Job Title')} at {exp.get('company', 'Company')}**"
                )
                st.markdown(f"{exp.get('dates', 'Dates')} | {exp.get('location', 'Location')}")
                if "responsibilities" in exp:
                    st.markdown("Responsibilities:")
                    for resp in exp["responsibilities"]:
                        st.markdown(f"- {resp}")
                st.markdown("---")

    # Display certificates
    if "certificates" in cv_data:
        st.markdown("### Certificates")
        st.markdown("  ||  ".join(cv_data["certificates"]))

    # Display skills
    if "skills" in cv_data:
        st.markdown("### Skills")
        st.markdown(", ".join(cv_data["skills"]))

    # Display other information
    if "others" in cv_data:
        st.markdown("### Additional Information")
        for item in cv_data["others"]:
            st.markdown(f"- {item}")

    st.markdown("</div>", unsafe_allow_html=True)
