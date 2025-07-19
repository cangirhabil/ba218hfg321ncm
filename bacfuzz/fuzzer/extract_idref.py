from bs4 import BeautifulSoup
import re

def find_potential_ids(html_content):
    """
    Find values that might represent database primary keys in HTML.

    Args:
        html_content (str): HTML content as string

    Returns:
        dict: A dictionary with categories of found IDs
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    params = list()
    values = list()

    # 1. Find hidden inputs with names suggesting IDs
    for input_tag in soup.find_all('input', type='hidden'):
        name = input_tag.get('name', '').lower()
        if any(kw in name for kw in ['id', 'userid', 'itemid', 'pk']):
            params.append(input_tag.get('name'))
            values.append(input_tag.get('value'))

    # 2. Extract IDs from URL paths
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        # Match patterns like /users/123 or ?id=456
        matches = re.findall(r'/(\d+)(?=/|$)|[?&](?:id|user_id)=(\d+)', href)
        for match in matches:
            params.append("url_paths")
            values.append(match[0] or match[1])

    return params, values
