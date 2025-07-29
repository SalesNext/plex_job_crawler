from collections.abc import Iterable
from urllib.parse import urljoin

from salesnext_crawler.events import CrawlEvent, DataEvent, Event
from scrapy.http.response.html import HtmlResponse
from scrapy import Request
import json
import re
from pydantic import BaseModel
from plex_job_crawler.schema.recruit import Recruit, Features
from plex_job_crawler.schema.company import Company
    
def parse_recruit_detail(
    event: CrawlEvent[None, Event, HtmlResponse],
    response: HtmlResponse,
) -> Iterable[Event]:
    script = response.xpath("//script[@type='application/ld+json']/text()").get()
    json_data = json.loads(script)
    next_data = response.xpath("//script[@id='__NEXT_DATA__']/text()").get()
    next_data_json = json.loads(next_data)
    company_data = next_data_json.get('props', {}).get('pageProps', {}).get('data', {}).get('company', {})

    job = Recruit(
    source_job_url = response.url,
    job_id = response.url.split("/")[-2],
    job_company_id = company_data.get('id', ''),
    job_title = json_data.get('title', ''),
    job_category_id = event.metadata.get('category_id', ''),
    job_posted_at = json_data.get('datePosted', ''),
    job_employment_type = json_data.get('employmentType', ''),
    job_working_hour = json_data.get('workHours', '').strip(),
    job_benefit = json_data.get('benefits', ''),                                                                                                                                                                     
    job_company_name = json_data.get('hiringOrganization', {}).get('name', ''),
    job_company_country = json_data.get('jobLocation', {}).get('address', {}).get('addressCountry', ''),
    job_company_region = json_data.get('jobLocation', {}).get('address', {}).get('addressRegion', ''),
    job_company_locality = json_data.get('jobLocation', {}).get('address', {}).get('addressLocality', ''),
    job_address_street = json_data.get('jobLocation', {}).get('address', {}).get('streetAddress', ''),
    job_description = next_data_json.get('props', {}).get('pageProps', {}).get('data', {}).get('jobDetail', {}).get('jobDescriptionOption', None),
    job_company_postal_code = json_data.get('jobLocation', {}).get('address', {}).get('postalCode', ''),
    job_salary_unit = json_data.get('baseSalary', {}).get('value', {}).get('unitText', ''),
    job_max_salary = str(json_data.get('baseSalary', {}).get('value', {}).get('maxValue', '')),
    job_min_salary = str(json_data.get('baseSalary', {}).get('value', {}).get('minValue', '')),
    
    job_salary = str(json_data.get('baseSalary', {}).get('value', {}).get('value', '')),
    job_holiday = next_data_json.get('props', {}).get('pageProps', {}).get('data', {}).get('jobDetail', {}).get('holidayOption', None),
    job_requirement = next_data_json.get('props', {}).get('pageProps', {}).get('data', {}).get('jobDetail', {}).get('qualificationOption', None),
    job_welfare = next_data_json.get('props', {}).get('pageProps', {}).get('data', {}).get('jobDetail', {}).get('welfareOption', None),
    job_industry = next_data_json.get('props', {}) \
    .get('pageProps', {}) \
    .get('data', {}) \
    .get('occupation', {}) \
    .get('name', None)   
    )
    features = next_data_json.get('props', {}).get('pageProps', {}).get('data', {}).get('features', [])
    feat = []
    for feature in features:
        id = feature.get('id', '')
        name = feature.get('name', '')
        category = feature.get('category', '')
        feat.append(Features(id=id, name=name, category=category))
    job.job_features = feat
    company_url = ''
    all_urls = response.xpath("//a/@href").getall()
    for url in all_urls:
        if '/company/' in url:
            company_url = url
            break
    company = Company(
    company_id = company_data.get('id', ''),
    company_url = urljoin(response.url, company_url),
    company_address = company_data.get('addressLine', ''),
    company_name = company_data.get('name', ''),
    company_capital = company_data.get('companyDetail', {}).get('capitalStock', None),
    company_employee_count = company_data.get('companyDetail', {}).get('employeeNumber', None),
    company_establish_date = company_data.get('companyDetail', {}).get('establishmentDate', None),
    company_representative = company_data.get('companyDetail', {}).get('representativeName', None),
    company_business_main_client = company_data.get('companyDetail', {}).get('businessMainClient', None),
    company_postal_code = json_data.get('jobLocation', {}).get('address', {}).get('postalCode', ''),
    )
    
    yield DataEvent(
        "recruit", job
    )
    
    yield DataEvent(
        "company", company
    )