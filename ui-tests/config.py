import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    BASE_URL = os.getenv("OZON_BASE_URL", "https://www.ozon.ru")
    SEARCH_QUERY = os.getenv("SEARCH_QUERY", "беспроводные наушники")
    PAGE_LOAD_TIMEOUT = int(os.getenv("PAGE_LOAD_TIMEOUT", "30000"))
    ELEMENT_TIMEOUT = int(os.getenv("ELEMENT_TIMEOUT", "10000"))
    IMPLICIT_WAIT = int(os.getenv("IMPLICIT_WAIT", "5000"))
