from requests import get
from bs4 import BeautifulSoup
from collections import Counter
import time

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
        start_time = time.time()
        response = get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        end_time = time.time()
        page_load_time = end_time - start_time
        results["page_load_time"] = round(page_load_time, 2)
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

     # Measure number of CSS files
    css_files_count = len(soup.find_all('link', {'rel': 'stylesheet'}))
    results["css_files_count"] = css_files_count

    # Measure number of JavaScript files
    js_files_count = len(soup.find_all('script', {'src': True}))
    results["js_files_count"] = js_files_count

    # Measure number of HTTP requests
    http_requests_count = len(soup.find_all(['img', 'script', 'link', 'a', 'form', 'iframe']))
    results["http_requests_count"] = http_requests_count

     # Measure number of redirects
    redirect_count = len(response.history)
    results["redirect_count"] = redirect_count

    # Analyze Total Number of Resources Loaded
    total_resources = len(soup.find_all(['img', 'script', 'link']))
    results['img'] = len(soup.find_all(['img']))
    results['script'] = len(soup.find_all(['script']))
    results['link'] = len(soup.find_all(['link']))
    results["total_resources"] = total_resources

     # Analyze AMP status
    amp_link = soup.find('link', {'rel': 'amphtml'})
    results['amp_status'] = "Yes" if amp_link else "No"

    try:
        psi_url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}"
        psi_response = get(psi_url)
        psi_data = psi_response.json()
        if "loadingExperience" in psi_data:
            loading_experience = psi_data["loadingExperience"]
            results["first_contentful_paint"] = loading_experience.get("metrics", {}).get("FIRST_CONTENTFUL_PAINT_MS", -1)
            results["time_to_interactive"] = loading_experience.get("metrics", {}).get("FIRST_INTERACTIVE_MS", -1)
            results["cumulative_layout_shift"] = psi_data.get("lighthouseResult", {}).get("audits", {}).get("cumulative-layout-shift", {}).get("numericValue", -1)
    except Exception as e:
        results["error_psi"] = f"Error fetching PageSpeed Insights data: {e}"

    # Additional SEO analysis
    # You can add more SEO checks here based on your requirements

    return results
