import json
from enum import Enum
from typing import Dict, List, Union

from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI


class EducationAlignment(Enum):
    BAD = "Bad"
    MODERATE = "Moderate"
    GOOD = "Good"


def analyze_job_description(
    job_description: str, user_skills: str, user_education: str, cv_text: str
) -> Dict[str, Union[int, List[str], str]]:
    llm = OpenAI(temperature=0.2, max_tokens=500)

    template = """
    Analyze the following job description and compare it with the user's skills, education, and CV:

    Job Description:
    {job_description}

    User's Skills (separated by comma):
    {user_skills}

    User's Education:
    {user_education}
    
    User's CV:
    {cv_text}

    Provide a detailed analysis including:
    1. match_percentage: Overall match percentage (between 0 and 100)
    2. matching_skills: Key skills that match the job requirements
    3. skills_to_develop: Skills that the user may need to develop
    4. education_alignment: How well the user's education aligns with the job (Bad, Moderate, or Good)
    5. cv_summary: Answer this question, why is the applicant is a good fit for this role (use the inforamtion from applicant cv and from job description)

    Format the response as a JSON object with the following keys:
    {{
    "match_percentage": int,
    "matching_skills": [],
    "skills_to_develop": [],
    "education_alignment": "",
    "cv_summary": ""
    }}
    """

    prompt = PromptTemplate(
        input_variables=["job_description", "user_skills", "user_education", "cv_text"],
        template=template,
    )

    chain = LLMChain(llm=llm, prompt=prompt)

    response = chain.run(
        job_description=job_description,
        user_skills=user_skills,
        user_education=user_education,
        cv_text=cv_text,
    )

    json_start = response.find("{")
    json_end = response.rfind("}") + 1

    if json_start != -1 and json_end != -1:
        json_str = response[json_start:json_end]
        try:
            result = json.loads(json_str)
            return {
                "match_percentage": parse_match_percentage(result.get("match_percentage")),
                "matching_skills": result.get("matching_skills", []),
                "skills_to_develop": result.get("skills_to_develop", []),
                "education_alignment": parse_education_alignment(result.get("education_alignment")),
                "cv_summary": result.get("cv_summary", ""),
            }
        except json.JSONDecodeError:
            return {"error": "Failed to parse JSON response"}
    else:
        return {"error": "No valid JSON found in the response"}


def parse_match_percentage(percentage: Union[int, str, None]) -> int:
    if isinstance(percentage, int):
        return max(0, min(100, percentage))
    elif isinstance(percentage, str):
        try:
            return max(0, min(100, int(percentage)))
        except ValueError:
            return 0
    return 0


def parse_education_alignment(alignment: str) -> EducationAlignment:
    try:
        return EducationAlignment(alignment.capitalize())
    except ValueError:
        return EducationAlignment.BAD
