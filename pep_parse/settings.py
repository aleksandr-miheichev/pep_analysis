from pathlib import Path

BOT_NAME = "pep_parse"

SPIDER_MODULES = ["pep_parse.spiders"]

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    "pep_parse.pipelines.PepParsePipeline": 300,
}

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

OUTPUT_FOLDER = 'results'

FEEDS = {
    f'{OUTPUT_FOLDER}/pep_%(time)s.csv': {
        'format': 'csv',
        'fields': ['number', 'name', 'status'],
        'overwrite': True
    }
}

BASE_DIR = Path(__file__).parent.parent
