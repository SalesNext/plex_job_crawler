from collections.abc import Iterable
from urllib.parse import urljoin

from salesnext_crawler.events import CrawlEvent, DataEvent, Event
from scrapy.http.response.html import HtmlResponse
from scrapy import Request
from urllib.parse import urljoin
import re
from pydantic import BaseModel

from plex_job_crawler.parser.parse_recruit_detail import parse_recruit_detail
    
def parse_recruit_list(
    event: CrawlEvent[None, Event, HtmlResponse],
    response: HtmlResponse,
) -> Iterable[Event]:
    
    next_page = response.xpath("//a[@aria-label = 'Next page']/@href").get()
    
    url = re.sub(r"\?page=\d+", "", response.url)
    print(urljoin(url, next_page))
    if next_page:
        yield CrawlEvent(
            request = Request(urljoin(url, next_page)),
            metadata = event.metadata,
            callback = parse_recruit_list,
        )
    blocks = response.xpath("//div[@class='p-md lg:p-lg']")
    urls = []
    for block in blocks:
        recruit_url = block.xpath(".//a/@href").get()
        urls.append(recruit_url)
        if f'{event.metadata["category_id"]}/job' in recruit_url:
            urls.append(recruit_url)
        job_id = recruit_url.split("/")[-2]    
        yield CrawlEvent(  
            request = Request('https://www.plex-job.com'+ recruit_url),
            metadata = event.metadata,
            callback = parse_recruit_detail,
            )
        
         
    
    