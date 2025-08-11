from collections.abc import Iterable
from urllib.parse import urljoin

from salesnext_crawler.events import CrawlEvent, DataEvent, Event
from scrapy.http.response.html import HtmlResponse
from scrapy import Request
from plex_job_crawler.parser.parse_recruit_list import parse_recruit_list
import re
from pydantic import BaseModel


    
def parse_recruit_category(
    event: CrawlEvent[None, Event, HtmlResponse],
    response: HtmlResponse,
) -> Iterable[Event]:
    
    categories = response.xpath("//div[@class='pb-2xl border-b border-gray-200']//a[@class='undefined tap-highlight-on']//@href").getall()
    for category in categories:
        category_id = category.split("/")[-2]
        url = urljoin(response.url, category)
        
        # if url == 'https://www.plex-job.com/driver/':
        #     continue
        yield CrawlEvent(
            request = Request(url),
            metadata= {'crawled_recruit_ids': event.metadata.get('crawled_recruit_ids', []), 'crawled_company_ids': event.metadata.get('crawled_company_ids', []), 'category_id': category_id},
            callback = parse_recruit_list,
        )
        
    