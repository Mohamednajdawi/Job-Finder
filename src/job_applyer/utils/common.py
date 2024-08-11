from typing import List

from pydantic import BaseModel, Field, HttpUrl


class JobSearchInput(BaseModel):
    job_title: str = Field(..., description="The job title to search for")
    country: str = Field(..., description="The country to search jobs in")
    number_of_jobs: int = Field(..., ge=1, description="Number of job listings to fetch")


class Job(BaseModel):
    title: str = Field(..., description="The title of the job posting")
    company: str = Field(..., description="The name of the company offering the job")
    description: str = Field(..., description="The full job description")
    link: HttpUrl = Field(..., description="The URL of the job posting on LinkedIn")


class JobSearchOutput(BaseModel):
    jobs: List[Job]
    total_results: int = Field(..., description="Total number of job listings found")
    search_criteria: JobSearchInput = Field(..., description="The criteria used for this search")
