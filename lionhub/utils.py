import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_url_response(url: str, timeout: tuple = (1, 1), **kwags) -> requests.Response:
    try:
        response = requests.get(url, timeout=timeout, **kwags)
        response.raise_for_status()
        return response
    except requests.exceptions.ConnectTimeout:
        raise TimeoutError(f"Timeout: requesting the url responses took too long (>{timeout[0]}) seconds.")
    except requests.exceptions.ReadTimeout:
        raise TimeoutError(f"Timeout: reading the url responses took too long (>{timeout[1]}) seconds.")
    except Exception as e:
        raise e

def get_url_content(url):
    response = get_url_response(url)
    soup = BeautifulSoup(response.text, features="html.parser")
    text_content = ' '.join([p.get_text() for p in soup.find_all('p')])
    return text_content

def to_df(items):
    df = pd.DataFrame(items).dropna()
    df.reset_index(drop=True, inplace=True)
    return df

