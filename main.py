from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import sys

def get_html_response(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    Return text content if response is of type HTML/XML
    Return None otherwise
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error(f'Error during requests to {url} : {str(e)}')
        return None


def is_good_response(resp):
    """
    Returns True if the response is of type HTML
    Return False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)

def scrape_html(html, attribute_class=None):
	"""
	Scrapes an html response pivotting on its h3 element
	Print all h3 elements' text if no attribute_class is given
	Otherwise print only h3 elements' with given attribute_class
	Failing that, returns an error message
	"""
	response = get_html_response(html)

	if response is not None:
		html = BeautifulSoup(response, 'html.parser')

		h3List = html.find_all('h3')
		for h3 in h3List:
			# Print only the h3's that have the 'class' attribute
			if attribute_class is not None:
				aList = h3.find_all('a', attrs={"class" : attribute_class})
				for a in aList:
					print(a.text)
			# Print all h3's
			else:
				print(h3.text)
	else:
		return("Connection to designated url failed")

def log_error(error):
	"""
	Error logger
	"""
	print(error)


if __name__ == '__main__':
	scrape_html('https://stackoverflow.com', 'question-hyperlink')