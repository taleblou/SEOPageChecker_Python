# **SEO Analysis and Website Insights Tool**

This Python script provides a comprehensive analysis of a website's Search Engine Optimization (SEO) and performance metrics. It fetches a webpage's HTML, extracts key elements, and evaluates various SEO factors.

## **Features**

* **Title and Meta Description Analysis**:  
  * Checks title tag length and quality.  
  * Evaluates meta description length and quality.  
  * Counts keywords in the title and description.  
* **Content Analysis**:  
  * Word count and keyword density.  
  * Text-to-HTML ratio.  
  * Duplicate phrases detection.  
* **Heading and Hierarchy**:  
  * Counts H1 and H2 tags.  
  * Validates header tag hierarchy.  
* **Image Optimization**:  
  * Counts images with and without `alt` attributes.  
  * Identifies lazy-loaded and large images.  
* **Link Analysis**:  
  * Counts internal, external, and broken links.  
  * Analyzes anchor texts and affiliate links.  
* **Structured Data**:  
  * Detects structured data scripts and schema types.  
  * Validates Open Graph and Twitter card tags.  
* **Performance Metrics**:  
  * Measures page load time.  
  * Checks gzip compression.  
* **Mobile-Friendliness**:  
  * Detects viewport meta tag.  
* **Security and Accessibility**:  
  * Checks HTTPS usage.  
  * Evaluates cookie banners and ARIA roles.  
* **Sitemaps and Robots.txt**:  
  * Verifies sitemap and robots.txt availability.  
* **Media Content**:  
  * Counts video and audio elements.  
* **Additional Checks**:  
  * Language and charset detection.  
  * Favicon presence.  
  * Header tag hierarchy validation.  
  * Social proof elements.

## **Prerequisites**

* Python 3.x

Install the required libraries using:  
bash  
Copy code  
`pip install requests beautifulsoup4 pandas`

* 

## **Usage**

  **Update the keywords**: Modify the `keywords` list in the `analyze_seo` function to match your specific focus.

**Run the script**:  
bash  
Copy code  
`python main.py`

 

**Analyze a webpage**: Replace `url` with the target webpage URL:  
python  
Copy code  
`html, load_time = fetch_page("https://example.com")`

`if html:`

    `seo_data = analyze_seo(html, "https://example.com")`

    `print(seo_data)`

 
  **Save results to a file**: Export the SEO data to a CSV or JSON file using `pandas`.

## **Sample Output**

A dictionary summarizing the SEO metrics, e.g.:

json

Copy code

`{`

  `"url": "https://example.com",`

  `"title": "Example Page",`

  `"title_length": 12,`

  `"title_quality": "Good",`

  `"meta_description": "This is an example meta description.",`

  `"meta_description_length": 48,`

  `"meta_description_quality": "Good",`

  `"h1_count": 2,`

  `"h2_count": 5,`

  `"image_count": 10,`

  `"images_with_alt": 8,`

  `"broken_links": 1,`

  `"https": "Yes",`

  `"mobile_friendly": "Yes",`

  `"page_load_time": 1.42,`

  `...`

`}`

## **Notes**

* **Timeouts**: The script uses a timeout for network requests to prevent long waits.  
* **Error Handling**: Gracefully handles network and parsing errors.  
* **Customization**: Update the keywords and checks as needed for specific use cases.

## **Limitations**

* The script checks for broken links but doesn't validate complex JavaScript-rendered pages.  
* Duplicate content detection across multiple pages requires additional functionality.

