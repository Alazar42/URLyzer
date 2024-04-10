from requests import get
from bs4 import BeautifulSoup
from collections import Counter

def analyze_url(url):
    """
    Analyzes a given URL for SEO optimization factors.

    Args:
        url: The URL to be analyzed.

    Returns:
        A dictionary containing SEO analysis results.
    """
    results = {}

    # Fetch the webpage content
    try:
        response = get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
    except Exception as e:
        results["error"] = f"Error fetching webpage: {e}"
        return results

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Analyze Title tag
    title = soup.find('title')
    if title:
        results["title"] = title.text.strip()
    else:
        results["title"] = "Missing Title tag"

    # Analyze meta description tag
    description = soup.find('meta', attrs={'name': 'description'})
    if description:
        results["description"] = description['content'].strip()
    else:
        results["description"] = "Missing meta description tag"

   # Analyze Headings (H1, H2, etc.)
    headings = soup.find_all(['h1', 'h2', 'h3'])
    if headings:
        results["headings"] = [heading.text.strip() for heading in headings]
    else:
        results["headings"] = []


    # Analyze Internal Links (basic check)
    internal_links = set()
    for link in soup.find_all('a'):
        if link.has_attr('href') and not link['href'].startswith(('http', '#')):
            internal_links.add(link['href'])
    results["internal_links"] = list(internal_links)

    # Analyze Images with missing alt attribute
    images_no_alt = []
    for img in soup.find_all('img'):
        if not img.has_attr('alt'):
            images_no_alt.append(img['src'])
    results["images_no_alt"] = images_no_alt

    # Analyze Keyword Usage (basic check - count words in text content)
    text = soup.get_text(separator=' ').lower()
    word_counts = Counter(text.split())
    top_keywords = word_counts.most_common(10)  # Top 10 most frequent words
    results["top_keywords"] = top_keywords

    # Analyze Mobile-friendliness (basic check - look for viewport meta tag)
    viewport = soup.find('meta', attrs={'name': 'viewport'})
    results["mobile_friendly"] = "Yes" if viewport else "No (may not be mobile-friendly)"

    # Analyze External Links (basic check)
    external_links = []
    for link in soup.find_all('a'):
        if link.has_attr('href') and link['href'].startswith(('http', 'https')):
            external_links.append(link['href'])
    results["external_links"] = external_links

    # Analyze Page Load Time (not implemented here - requires performance testing tools)
    # ... (code to measure page load time)
    # results["page_load_time"] = page_load_time_in_seconds

    return results