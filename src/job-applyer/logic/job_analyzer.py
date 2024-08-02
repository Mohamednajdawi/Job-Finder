from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import OpenAI


def analyze_job_description(job_description, user_skills, user_education):
    llm = OpenAI(temperature=0.7)

    template = """
    Analyze the following job description and compare it with the user's skills and education:

    Job Description:
    {job_description}

    User's Skills:
    {user_skills}

    User's Education:
    {user_education}

    Provide a brief analysis of how well the user's background matches the job requirements:
    """

    prompt = PromptTemplate(
        input_variables=["job_description", "user_skills", "user_education"],
        template=template,
    )

    chain = LLMChain(llm=llm, prompt=prompt)

    return chain.run(
        job_description=job_description, user_skills=user_skills, user_education=user_education
    )
