import json

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import OpenAI


def analyze_job_description(job_description, user_skills, user_education):
    llm = OpenAI(temperature=0.2, max_tokens=500)

    template = """
    Analyze the following job description and compare it with the user's skills and education:

    Job Description:
    {job_description}

    User's Skills:
    {user_skills}

    User's Education:
    {user_education}

    Provide a detailed analysis including:
    1. Overall match percentage, between 0 and 100
    2. Key skills that match the job requirements
    3. Skills that the user may need to develop
    4. How well the user's education aligns with the job, options: [Bad, Moderate, Good]

    Format the response as a JSON object with the following keys:
    match_percentage, matching_skills, skills_to_develop, education_alignment 
    """

    prompt = PromptTemplate(
        input_variables=["job_description", "user_skills", "user_education"],
        template=template,
    )

    chain = LLMChain(llm=llm, prompt=prompt)

    response = chain.run(
        job_description=job_description, user_skills=user_skills, user_education=user_education
    )
    json_str = response[response.find('{'): response.find('}') + 1]

    # Remove all newlines and extra spaces
    json_str_clean = ''.join(json_str.split())

    # Parse the cleaned string into a dictionary
    result = json.loads(json_str_clean)

    return result
