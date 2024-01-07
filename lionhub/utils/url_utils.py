from bs4 import BeautifulSoup
import requests

def get_url_response(url: str, timeout: tuple = (1, 1), **kwargs) -> requests.Response:
    # Sends a GET request to a URL and returns the response.
    try:
        response = requests.get(url, timeout=timeout, **kwargs)
        response.raise_for_status()
        return response
    except requests.exceptions.ConnectTimeout:
        raise TimeoutError(f"Timeout: requesting >{timeout[0]} seconds.")
    except requests.exceptions.ReadTimeout:
        raise TimeoutError(f"Timeout: reading >{timeout[1]} seconds.")
    except Exception as e:
        raise e
    
def get_url_content(url: str) -> str:
    # Extracts text content from paragraphs in the given URL.
    response = get_url_response(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return ' '.join(p.get_text() for p in soup.find_all('p'))
