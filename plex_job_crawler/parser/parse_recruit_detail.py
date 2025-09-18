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
        source_job_url=response.url,
        job_id=response.url.split("/")[-2],
        job_company_id=company_data.get('id', None),
        job_title=json_data.get('title', None),
        job_category_id=event.metadata.get('category_id', None),
        job_posted_at=json_data.get('datePosted', None),
        job_employment_type=json_data.get('employmentType', None),
        job_working_hour=(json_data.get('workHours', None) or "").strip(),
        job_benefit=json_data.get('benefits', None),
        job_company_name=(json_data.get('hiringOrganization') or {}).get('name'),
        job_company_country=((json_data.get('jobLocation') or {}).get('address') or {}).get('addressCountry'),
        job_company_region=((json_data.get('jobLocation') or {}).get('address') or {}).get('addressRegion'),
        job_company_locality=((json_data.get('jobLocation') or {}).get('address') or {}).get('addressLocality'),
        job_address_street=((json_data.get('jobLocation') or {}).get('address') or {}).get('streetAddress'),
        job_description=((((next_data_json.get('props') or {}).get('pageProps') or {}).get('data') or {}).get('jobDetail') or {}).get('jobDescriptionOption'),
        job_company_postal_code=((json_data.get('jobLocation') or {}).get('address') or {}).get('postalCode'),
        job_salary_unit=((json_data.get('baseSalary') or {}).get('value') or {}).get('unitText'),
        job_max_salary=str(((json_data.get('baseSalary') or {}).get('value') or {}).get('maxValue')),
        job_min_salary=str(((json_data.get('baseSalary') or {}).get('value') or {}).get('minValue')),
        job_salary=str(((json_data.get('baseSalary') or {}).get('value') or {}).get('value')),
        job_holiday=((((next_data_json.get('props') or {}).get('pageProps') or {}).get('data') or {}).get('jobDetail') or {}).get('holidayOption'),
        job_requirement=((((next_data_json.get('props') or {}).get('pageProps') or {}).get('data') or {}).get('jobDetail') or {}).get('qualificationOption'),
        job_welfare=((((next_data_json.get('props') or {}).get('pageProps') or {}).get('data') or {}).get('jobDetail') or {}).get('welfareOption'),
        job_industry=(((next_data_json.get('props') or {}).get('pageProps') or {}).get('data') or {}).get('occupation', {}).get('name'),
    )
    
    features = next_data_json.get('props', {}).get('pageProps', {}).get('data', {}).get('features', [])
    feat = []
    for feature in features:
        id = feature.get('id', None)
        name = feature.get('name', None)
        category = feature.get('category', None)
        feat.append(Features(id=id, name=name, category=category))
    job.job_features = feat
    company_url = None
    all_urls = response.xpath("//a/@href").getall()
    company_capital = (company_data.get('companyDetail') or {}).get('capitalStock')

    for url in all_urls:
        if '/company/' in url:
            company_url = url
            break
    company = Company(
    company_id = company_data.get('id', None),
    company_url = urljoin(response.url, company_url),
    company_address = response.xpath('//a[contains(@href, "https://www.google.com/maps/search/?api")]/text()').getall()[-1],
    company_name = company_data.get('name', None),
    company_capital = company_capital or None,
    company_employee_count = (company_data.get('companyDetail') or {}).get('employeeNumber'),
    company_establish_date = (company_data.get('companyDetail') or {}).get('establishmentDate'),
    company_representative = (company_data.get('companyDetail') or {}).get('representativeName'),
    company_business_main_client = (company_data.get('companyDetail') or {}).get('businessMainClient'),
    company_postal_code = ((json_data.get('jobLocation') or {}).get('address') or {}).get('postalCode'),
    )
    
    yield DataEvent(
        "recruit", job
    )
    
    yield DataEvent(
        "company", company
    )