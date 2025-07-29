from pydantic import BaseModel
from typing import Optional, List


class Features(BaseModel):
    id : Optional[str] = None
    name : Optional[str] = None
    category : Optional[str] = None

class Recruit(BaseModel):
    source_job_url : Optional[str] = None   
    job_id : Optional[str] = None
    job_company_id : Optional[str] = None
    job_title : Optional[str] = None
    job_posted_at : Optional[str] = None
    job_employment_type : Optional[str] = None
    job_working_hour : Optional[str] = None
    job_posted_at : Optional[str] = None
    job_employment_type: Optional[str] = None
    job_working_hour: Optional[str] = None
    job_benefit : Optional[str] = None
    job_description : Optional[str] = None
    job_company_name : Optional[str] = None
    job_company_country : Optional[str] = None
    job_company_region : Optional[str] = None
    job_company_locality : Optional[str] = None
    job_address_street : Optional[str] = None
    job_company_postal_code : Optional[str] = None
    job_salary_unit : Optional[str] = None
    job_max_salary : Optional[str] = None
    job_min_salary : Optional[str] = None
    job_address : Optional[str] = None
    job_salary : Optional[str] = None
    job_holiday : Optional[str] = None
    job_requirement : Optional[str] = None
    job_welfare : Optional[str] = None
    job_industry : Optional[str] = None
    job_features : Optional[List[Features]] = None