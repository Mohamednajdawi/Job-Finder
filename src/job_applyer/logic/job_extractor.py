import json
from enum import Enum
from typing import List, Union

from langchain.chains.llm import LLMChain

# from langchain_openai import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate


class ApplyingMethod(Enum):
    EMAIL = "Email"
    LINK = "Link"
    OTHER = "Other"


class RemoteWorkCompatibility(Enum):
    FULLY_REMOTE = "Fully Remote"
    HYBRID = "Hybrid"
    ON_SITE = "On-Site"
    FLEXIBLE = "Flexible"


def job_description_data_extract(job_description: str) -> dict:
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.1, max_tokens=2000)

    template = """
    Analyze the following job description and extract relevant information:

    Job Description:
    {job_description}

    Extract and structure the information into the following categories:
    1. Salary: Any integer or range (e.g., 50000, [60000, 80000])
    2. Applying method: Email, Link, or Other
    3. Remote Work Compatibility: Fully Remote, Hybrid, On-Site, or Flexible
    4. Job additional benefits: List of strings

    Format the response as a JSON object with the following keys:
    salary, applying_method, remote_work_compatibility, additional_benefits
    Ensure that the response is a valid JSON object and follows this template:
    
    {{
    "salary": null,
    "applying_method": "",
    "remote_work_compatibility": "",
    "additional_benefits": []
    }}

    If any information is missing, use null for that field.
    """

    prompt = PromptTemplate(
        input_variables=["job_description"],
        template=template,
    )

    chain = LLMChain(llm=llm, prompt=prompt)

    response = chain.run({"job_description": job_description})
    json_start = response.find("{")
    json_end = response.rfind("}") + 1

    if json_start != -1 and json_end != -1:
        json_str = response[json_start:json_end]
        try:
            result = json.loads(json_str)
            return {
                "salary": parse_salary(result.get("salary")),
                "applying_method": parse_applying_method(result.get("applying_method")),
                "remote_work_compatibility": parse_remote_work(
                    result.get("remote_work_compatibility")
                ),
                "additional_benefits": result.get("additional_benefits", []),
            }
        except json.JSONDecodeError:
            return {"error": "Failed to parse JSON response"}
    else:
        return {"error": "No valid JSON found in the response"}


def parse_salary(salary: Union[int, List[int], None]) -> Union[int, List[int], None]:
    if isinstance(salary, int):
        return salary
    elif isinstance(salary, list) and len(salary) == 2:
        return [int(salary[0]), int(salary[1])]
    return None


def parse_applying_method(method: str) -> ApplyingMethod:
    try:
        return ApplyingMethod(method.capitalize())
    except (ValueError, AttributeError):
        return ApplyingMethod.OTHER


def parse_remote_work(compatibility: str) -> RemoteWorkCompatibility:
    try:
        return RemoteWorkCompatibility(compatibility.replace(" ", "_").upper())
    except (ValueError, AttributeError):
        return RemoteWorkCompatibility.ON_SITE
