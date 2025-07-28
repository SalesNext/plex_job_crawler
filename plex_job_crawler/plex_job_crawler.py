from collections.abc import Iterable
from enum import Enum
from typing import Optional
from salesnext_crawler.crawler import ScrapyCrawler
from salesnext_crawler.events import CrawlEvent, Event, SitemapEvent
from scrapy import Request
from plex_job_crawler.parser.parse_recruit_category import parse_recruit_category
import pyarrow as pa

class PlexJobCrawler(ScrapyCrawler):
   def __init__(
       self,
       daily: bool = False
   ):
       self.daily = daily
   def start(self) -> Iterable[Event]:
       crawled_company_ids = []
       crawled_recruit_ids = []
       if self.daily:
        crawled_recruit_table : pa.Table = self.readers["recruit"].read()
        crawled_recruit_ids = crawled_recruit_table.select(["job_id"]).drop_null().to_pydict()["job_id"]
        
        crawled_company_table: pa.Table = self.readers["company"].read()
        crawled_company_ids = crawled_company_table.select(["company_id"]).drop_null().to_pydict()["company_id"]
        
       yield CrawlEvent(
           request = Request("https://www.plex-job.com/"),
           metadata= {'crawled_recruit_ids': crawled_recruit_ids,
                      'crawled_company_ids': crawled_company_ids},   
           callback= parse_recruit_category
       )