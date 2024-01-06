import os
import dotenv
dotenv.load_dotenv()

from typing import Any, Dict

from lionagi import lcall
from ..utils import get_url_response, get_url_content


class GoogleSearch:
    api_key = os.getenv('GOOGLE_API_KEY')
    search_engine = os.getenv('GOOGLE_CSE_ID')
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
        
        search_url = search_url or cls.search_url
        url = search_url.format(
            key=api_key or cls.api_key, 
            engine=search_engine or cls.search_engine, 
            query=query, 
            start=start
        )
        response = get_url_response(url, timeout=timeout)
        response_dict = response.json()
        items = response_dict.get('items')[:num]
        if content:
            items = lcall(items, cls._get_search_item_field, dropna=True)
        
        return items
