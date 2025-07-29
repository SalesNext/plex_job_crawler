from pydantic import BaseModel
from typing import Optional

class Company(BaseModel):
    company_id: Optional[str] = None
    company_url: Optional[str] = None
    company_name: Optional[str] = None  
    company_address: Optional[str] = None
    company_capital: Optional[str] = None
    company_employee_count: Optional[str] = None
    company_establish_date: Optional[str] = None
    company_representative: Optional[str] = None
    company_business_main_client: Optional[str] = None
    company_postal_code : Optional[str] = None
    