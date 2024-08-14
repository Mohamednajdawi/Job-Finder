import json

from langchain.chains.llm import LLMChain

# from langchain_openai import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate


def cv_data_extract(cv_text):
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.1, max_tokens=2000)

    template = """
    Analyze the following CV and extract relevant information:

    CV Text:
    {cv_text}

    Extract and structure the information into the following categories:
    1. Meta Data: Name, contact information, and any other identifying details
    2. Summary: A brief overview of the candidate's professional profile as str
    3. Education: Academic qualifications, institutions, and graduation dates
    4. Experience: Work history, including company names, job titles, dates, and key responsibilities
    5. Certificates: All the mentioned certificates as List[str]
    6. Skills: Technical skills, soft skills, and any other relevant competencies as List[str]
    7. Others: Any additional information such as certifications, awards, or volunteer work as List[str]

    Format the response as a JSON object with the following keys:
    meta_data, summary, education, experience, skills, others
    Ensure that the response is a valid JSON object and to follow this template (if any information is missing fill with None):
    
    {{
    "meta_data": {{
        "name": "",
        "contact_information": {{
            "location": "",
            "phone_number": "",
            "email": "",
            "linkedin": ""
        }}
    }},
    "summary": "",
    "education": [
        {{
            "institution": "",
            "degree": "",
            "major": "",
            "dates": ""
        }}
    ],
    "experience": [
        {{
            "company": "",
            "job_title": "",
            "dates": "",
            "location": "",
            "responsibilities": [
                ""
            ]
        }}
    ],
    "certificates":[
        ""
    ],
    "skills": [
        ""
    ],
    "others": [
        ""
    ]
    }}
    """

    prompt = PromptTemplate(
        input_variables=["cv_text"],
        template=template,
    )

    chain = LLMChain(llm=llm, prompt=prompt)

    response = chain.run({"cv_text": cv_text})
    # Find the start and end of the JSON object
    json_start = response.find("{")
    json_end = response.rfind("}") + 1

    if json_start != -1 and json_end != -1:
        json_str = response[json_start:json_end]
        try:
            result = json.loads(json_str)
            print("Correctly parsed JSON")
            return result
        except json.JSONDecodeError:
            return {"error": "Failed to parse JSON response"}
    else:
        return {"error": "No valid JSON found in the response"}
