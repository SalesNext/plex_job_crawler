from collections.abc import Iterable
from urllib.parse import urljoin

from salesnext_crawler.events import CrawlEvent, DataEvent, Event
from scrapy.http.response.html import HtmlResponse
from scrapy import Request

import re
from pydantic import BaseModel

from plex_job_crawler.parser.parse_recruit_detail import parse_recruit_detail
    
def parse_recruit_list(
    event: CrawlEvent[None, Event, HtmlResponse],
    response: HtmlResponse,
) -> Iterable[Event]:
    
    pages = response.xpath("//a[@class='h-full w-full p-sm inline-block text-center text-sm']/text()").getall()
    if pages:
        max_page = pages[-1]
        for page in range(2, int(max_page) +1):
            yield CrawlEvent(
                request=Request(f"{response.url}?page={page}"),
                metadata= event.metadata,
                callback=parse_recruit_list,
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
        
         
    
    