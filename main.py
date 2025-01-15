import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def fetch_page(url):
    """Fetch the HTML content and load time of the given URL."""
    try:
        start = time.time()
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        end = time.time()
        load_time = end - start
        return response.text, load_time
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None, None

def analyze_seo(html, url):
    """Analyze the SEO aspects of the HTML content."""
    soup = BeautifulSoup(html, "html.parser")
    seo_data = {'url': url}

    # Title Tag
    title_tag = soup.title.string if soup.title else None
    seo_data['title'] = title_tag
    seo_data['title_length'] = len(title_tag) if title_tag else 0
    seo_data['title_quality'] = "Good" if title_tag and 50 <= len(title_tag) <= 60 else "Needs Improvement"

    # Meta Description
    meta_description = soup.find("meta", attrs={"name": "description"})
    description_content = meta_description["content"] if meta_description and meta_description.get("content") else None
    seo_data['meta_description'] = description_content
    seo_data['meta_description_length'] = len(description_content) if description_content else 0
    seo_data['meta_description_quality'] = "Good" if description_content and 120 <= len(description_content) <= 160 else "Needs Improvement"

    # Keywords Count in Title and Description
    keywords = ['SEO', 'optimization', 'content']  # Example keywords to check
    seo_data['keywords_in_title'] = sum(keyword.lower() in (title_tag.lower() if title_tag else '') for keyword in keywords)
    seo_data['keywords_in_description'] = sum(keyword.lower() in (description_content.lower() if description_content else '') for keyword in keywords)

    # Headings (H1, H2)
    seo_data['h1_count'] = len(soup.find_all("h1"))
    seo_data['h2_count'] = len(soup.find_all("h2"))

    # Image Alt Tags
    images = soup.find_all("img")
    seo_data['image_count'] = len(images)
    seo_data['images_with_alt'] = sum(1 for img in images if img.get("alt"))
    seo_data['images_without_alt'] = seo_data['image_count'] - seo_data['images_with_alt']

    # Links
    links = soup.find_all("a", href=True)
    seo_data['link_count'] = len(links)
    seo_data['internal_links'] = sum(1 for link in links if url in link['href'])
    seo_data['external_links'] = seo_data['link_count'] - seo_data['internal_links']

    # Structured Data
    structured_data = soup.find_all("script", type="application/ld+json")
    seo_data['structured_data_count'] = len(structured_data)

    # Robots Meta Tag
    robots_meta = soup.find("meta", attrs={"name": "robots"})
    seo_data['robots_meta'] = robots_meta["content"] if robots_meta else "Not Found"

    # Canonical Tag
    canonical_link = soup.find("link", rel="canonical")
    seo_data['canonical_link'] = canonical_link["href"] if canonical_link else "Not Found"

    # Page Load Time
    _, load_time = fetch_page(url)
    seo_data['page_load_time'] = load_time

    # Mobile-Friendliness
    viewport = soup.find("meta", attrs={"name": "viewport"})
    seo_data['mobile_friendly'] = "Yes" if viewport else "No"

    # Favicon
    favicon = soup.find("link", rel="icon")
    seo_data['favicon'] = favicon["href"] if favicon else "Not Found"

    # Open Graph Tags
    og_tags = soup.find_all("meta", attrs={"property": lambda x: x and x.startswith("og:")})
    seo_data['og_tags_count'] = len(og_tags)

    # Twitter Card Tags
    twitter_tags = soup.find_all("meta", attrs={"name": lambda x: x and x.startswith("twitter:")})
    seo_data['twitter_tags_count'] = len(twitter_tags)

    # HTTPS Check
    seo_data['https'] = "Yes" if url.startswith("https") else "No"

    # Check for Broken Links
    broken_links = 0
    for link in links:
        try:
            response = requests.head(link['href'], timeout=5)
            if response.status_code >= 400:
                broken_links += 1
        except:
            broken_links += 1
    seo_data['broken_links'] = broken_links

    # Content Analysis
    body_text = soup.get_text()
    word_count = len(body_text.split())
    seo_data['word_count'] = word_count

    # Keyword Density
    for keyword in keywords:
        seo_data[f'keyword_density_{keyword}'] = (body_text.lower().count(keyword.lower()) / word_count) * 100 if word_count else 0

    # Language and Charset
    language = soup.find("html").get("lang") if soup.find("html") else None
    charset = soup.find("meta", attrs={"charset": True})
    seo_data['language'] = language if language else "Not Found"
    seo_data['charset'] = charset["charset"] if charset else "Not Found"

    # Sitemap Check
    sitemap_url = f"{url}/sitemap.xml"
    try:
        response = requests.head(sitemap_url, timeout=5)
        seo_data['sitemap'] = "Found" if response.status_code == 200 else "Not Found"
    except:
        seo_data['sitemap'] = "Not Found"

    # Robots.txt Check
    robots_url = f"{url}/robots.txt"
    try:
        response = requests.head(robots_url, timeout=5)
        seo_data['robots_txt'] = "Found" if response.status_code == 200 else "Not Found"
    except:
        seo_data['robots_txt'] = "Not Found"

    # Header Tag Hierarchy
    header_tags = [tag.name for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
    seo_data['header_tag_hierarchy'] = "Valid" if header_tags == sorted(header_tags, key=lambda x: int(x[1:])) else "Invalid"

    # Duplicate Title Check (Placeholder for cross-page analysis)
    existing_titles = set()  # Needs to be populated externally
    seo_data['duplicate_title'] = "Yes" if title_tag in existing_titles else "No"
    existing_titles.add(title_tag)

    # Text-to-HTML Ratio
    html_length = len(html)
    text_length = len(soup.get_text())
    seo_data['text_to_html_ratio'] = (text_length / html_length) * 100 if html_length else 0

    # Breadcrumb Navigation
    breadcrumbs = soup.find_all("nav", attrs={"aria-label": "breadcrumb"})
    seo_data['breadcrumbs'] = "Found" if breadcrumbs else "Not Found"

    # Pagination Tags
    next_link = soup.find("link", rel="next")
    prev_link = soup.find("link", rel="prev")
    seo_data['pagination_next'] = next_link["href"] if next_link else "Not Found"
    seo_data['pagination_prev'] = prev_link["href"] if prev_link else "Not Found"

    # Hreflang Tags
    hreflang_tags = soup.find_all("link", rel="alternate", hreflang=True)
    seo_data['hreflang_count'] = len(hreflang_tags)

    # AMP Validation
    amp_tag = soup.find("html", attrs={"amp": True})
    seo_data['amp'] = "Yes" if amp_tag else "No"

    # Content Freshness
    publish_date = soup.find("meta", attrs={"name": "article:published_time"})
    last_modified_date = soup.find("meta", attrs={"name": "article:modified_time"})
    seo_data['publish_date'] = publish_date["content"] if publish_date else "Not Found"
    seo_data['last_modified_date'] = last_modified_date["content"] if last_modified_date else "Not Found"

    # Schema Markup Types
    schema_types = []
    for script in structured_data:
        try:
            data = json.loads(script.string)
            if isinstance(data, dict) and "@type" in data:
                schema_types.append(data["@type"])
        except:
            pass
    seo_data['schema_types'] = ', '.join(schema_types) if schema_types else "None"

    # Specific Open Graph Tags
    og_image = soup.find("meta", attrs={"property": "og:image"})
    seo_data['og_image'] = og_image["content"] if og_image else "Not Found"

    # Twitter Card Image
    twitter_image = soup.find("meta", attrs={"name": "twitter:image"})
    seo_data['twitter_image'] = twitter_image["content"] if twitter_image else "Not Found"

    # Anchor Text Analysis
    anchor_texts = [link.get_text().strip() for link in links if link.get_text()]
    seo_data['anchor_texts'] = ', '.join(anchor_texts[:10])  # Example: Limit to first 10

    # JavaScript Errors
    inline_scripts = soup.find_all("script", type="text/javascript")
    seo_data['inline_script_count'] = len(inline_scripts)

    # External JavaScript Files
    external_scripts = soup.find_all("script", src=True)
    seo_data['external_script_count'] = len(external_scripts)

    # HTTP Status Code
    try:
        response = requests.head(url, timeout=5)
        seo_data['http_status_code'] = response.status_code
    except:
        seo_data['http_status_code'] = "Unknown"

    # Check for Duplicate Phrases
    phrases = body_text.split('.')
    duplicate_phrases = [phrase for phrase in phrases if phrases.count(phrase) > 1]
    seo_data['duplicate_phrases_count'] = len(duplicate_phrases)

    # XML Sitemap URL Count
    try:
        sitemap_response = requests.get(sitemap_url, timeout=5)
        if sitemap_response.status_code == 200:
            sitemap_soup = BeautifulSoup(sitemap_response.content, "xml")
            seo_data['sitemap_url_count'] = len(sitemap_soup.find_all("url"))
        else:
            seo_data['sitemap_url_count'] = 0
    except:
        seo_data['sitemap_url_count'] = "Error"

    # Accessibility Checks
    aria_roles = soup.find_all(attrs={"role": True})
    seo_data['aria_role_count'] = len(aria_roles)

    # Social Media Integration
    og_tags = ["og:title", "og:description", "og:image", "og:url"]
    twitter_tags = ["twitter:card", "twitter:title", "twitter:description", "twitter:image"]
    seo_data['og_tags_present'] = all(soup.find("meta", attrs={"property": tag}) for tag in og_tags)
    seo_data['twitter_tags_present'] = all(soup.find("meta", attrs={"name": tag}) for tag in twitter_tags)

    # Language Specification
    html_tag = soup.find("html")
    seo_data['lang_attribute'] = html_tag.get("lang", "Not Specified") if html_tag else "Not Found"

    # Duplicate Meta Description Check
    existing_descriptions = set()
    seo_data['duplicate_meta_description'] = "Yes" if description_content in existing_descriptions else "No"
    existing_descriptions.add(description_content)

    # Image Optimization
    large_images = [img for img in images if img.get("src") and "large" in img.get("src").lower()]
    seo_data['large_images_count'] = len(large_images)

    # HTTP Headers
    try:
        headers_response = requests.head(url, timeout=5)
        seo_data['cache_control'] = headers_response.headers.get("Cache-Control", "Not Found")
        seo_data['content_security_policy'] = headers_response.headers.get("Content-Security-Policy", "Not Found")
    except:
        seo_data['http_headers'] = "Error"

    # URL Structure Quality
    import re
    seo_data['url_length'] = len(url)
    seo_data['url_structure_quality'] = "Good" if re.match(r'^[a-zA-Z0-9\-\/]+$', url) and len(url) <= 100 else "Needs Improvement"

    # Content Hierarchy
    headings = [tag.name for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
    seo_data['heading_hierarchy'] = "Good" if headings == sorted(headings, key=lambda h: int(h[1:])) else "Needs Improvement"

    # Image Lazy Loading
    lazy_loaded_images = [img for img in images if img.get("loading") == "lazy"]
    seo_data['lazy_loaded_images'] = len(lazy_loaded_images)

    # Gzip Compression
    try:
        headers_response = requests.get(url, timeout=5)
        seo_data['gzip_compression'] = "Yes" if "gzip" in headers_response.headers.get("Content-Encoding", "") else "No"
    except:
        seo_data['gzip_compression'] = "Error"

    # Cookie Banner
    cookie_banner = soup.find("div", {"id": "cookie-banner"}) or soup.find(string="cookie")
    seo_data['cookie_banner'] = "Yes" if cookie_banner else "No"

    # Social Proof
    ratings = soup.find_all("div", {"class": "rating"}) or soup.find_all("span", {"class": "stars"})
    seo_data['social_proof_count'] = len(ratings)

    # Video and Audio Content
    videos = soup.find_all("video")
    audios = soup.find_all("audio")
    seo_data['video_count'] = len(videos)
    seo_data['audio_count'] = len(audios)

    # Affiliate Links
    affiliate_links = [link for link in links if "ref=" in link['href'] or "/affiliate/" in link['href']]
    seo_data['affiliate_links_count'] = len(affiliate_links)

    # Custom Fonts
    custom_fonts = soup.find_all("link", href=lambda href: href and "fonts" in href)
    seo_data['custom_fonts_count'] = len(custom_fonts)

    return seo_data

def generate_csv_report(urls, output_file):
    """Generate a CSV report for a list of URLs."""
    data = []
    for url in urls:
        print(f"Analyzing {url}...")
        html, _ = fetch_page(url)
        if html:
            seo_data = analyze_seo(html, url)
            data.append(seo_data)

    # Save to CSV
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)
    print(f"SEO report saved to {output_file}")

if __name__ == "__main__":
    # Input file containing URLs
    input_file = "urls.csv"  # Replace with your CSV file containing URLs
    output_file = "seo_report.csv"

    # Read URLs from CSV
    try:
        urls_df = pd.read_csv(input_file)
        urls = urls_df['url'].tolist()
    except Exception as e:
        print(f"Error reading input file {input_file}: {e}")
        urls = []

    # Generate SEO report
    if urls:
        generate_csv_report(urls, output_file)
    else:
        print("No URLs to analyze.")