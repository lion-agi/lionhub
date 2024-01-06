import os
from typing import Any, Dict

from lionagi import lcall
from ..utils.url_utils import get_url_response, get_url_content

key_scheme = 'GOOGLE_API_KEY'
engine_scheme = 'GOOGLE_CSE_ID'




class GoogleSearch:
    api_key = os.getenv(key_scheme)
    search_engine = os.getenv(engine_scheme)
    search_url = (
        """
        https://www.googleapis.com/customsearch/v1?key={key}&cx={engine}&q={query}&start={start}
        """
        )

    # get fields of a google search item 
    @classmethod
    def _get_search_item_field(cls, item: Dict[str, Any]) -> Dict[str, str]:
        try:
            long_description = item["pagemap"]["metatags"][0]["og:description"]
        except KeyError:
            long_description = "N/A"
        url = item.get("link")
        
        return {
            "title": item.get("title"),
            "snippet": item.get("snippet"),
            "url": item.get("link"),
            "long_description": long_description,
            "content": get_url_content(url)
        }
    
    # return as a list of dic
    # get the top num result from a google search with options of getting the search url content
    @classmethod
    def search_google(
        cls, 
        query: str =None, 
        search_url = None,
        api_key = None,
        search_engine=None,
        start: int = 1, 
        timeout: tuple = (0.5, 0.5), 
        content=True,
        num=5
        ):
        url = cls._format_search_url(
            url = search_url, query=query, api_key=api_key,
            search_engine=search_engine, start=start
            )
        response = get_url_response(url, timeout=timeout)
        response_dict = response.json()
        items = response_dict.get('items')[:num]
        if content:
            items = lcall(items, cls._get_search_item_field, dropna=True)
        return items

    @classmethod
    def _format_search_url(cls, url, api_key, search_engine, query, start):
        url = url or cls.search_url
        url = url.format(
            key=api_key or cls.api_key, 
            engine=search_engine or cls.search_engine, 
            query=query, 
            start=start
        )
        return url


