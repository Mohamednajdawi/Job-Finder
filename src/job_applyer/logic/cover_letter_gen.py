from langchain.chains.llm import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

# from langchain_openai import OpenAI


def generate_cover_letter(
    cv_text,
    applicant_name,
    job_title,
    job_company,
    job_description,
    job_analysis,
    user_skills,
    user_education,
):
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.3, max_tokens=1000)

    template = """
    Generate a detailed and compelling cover letter for the following job, highlighting the user's relevant skills, experience, education, and achievements. The cover letter should be well-structured with clear paragraphs and should be between 200-250 words long.
    Applicant Name:
    {applicant_name}

    Applicant CV:
    {cv_text}
    
    Job Title:
    {job_title}

    Job Company:
    {job_company}

    Job Description:
    {job_description}

    User's Skills:
    {user_skills}

    User's Education:
    {user_education}
    
    and here is some important summary of the CV:
    {job_analysis}

    Please follow this structure for the cover letter:
    1. Opening paragraph: Introduce yourself and express enthusiasm for the position.
    2. Body paragraph 1: Highlight relevant skills and how they align with the job requirements.
    3. Body paragraph 2: Discuss relevant work experience and specific accomplishments, if any
    4. Body paragraph 3: Mention educational background and any relevant academic achievements.
    5. Body paragraph 4: Describe personal achievements and how they demonstrate qualities valuable for the role, if any
    6. Closing paragraph: Reiterate interest, thank the reader, and express eagerness for an interview.
    7. Make sure the Cover Letter should be between 200-250 words long

    Important:
    Do not add any not mentioned information, at any cost
    Cover Letter:
    """

    prompt = PromptTemplate(
        input_variables=[
            "applicant_name",
            "cv_text",
            "job_title",
            "job_company",
            "job_description",
            "user_skills",
            "user_education",
            "job_analysis",
        ],
        template=template,
    )

    chain = LLMChain(llm=llm, prompt=prompt)

    return chain.run(
        applicant_name=applicant_name,
        cv_text=cv_text,
        job_title=job_title,
        job_company=job_company,
        job_description=job_description,
        user_skills=user_skills,
        user_education=user_education,
        job_analysis=job_analysis,
    )
