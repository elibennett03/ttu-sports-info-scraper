import json

import bs4
import requests
from playwright.sync_api import sync_playwright

URL = "https://www.ttusports.com/landing/index"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}
base_url = "https://www.ttusports.com"
response = requests.get(URL, headers=headers)
if response.status_code != 200:
    raise Exception(f"Failed to load page: {response.status_code}")

# print (response.text)

header_data = []
soup = bs4.BeautifulSoup(response.text, "html.parser")
all_images = soup.select(".slide-img img")
for img in all_images:
    # print(img)
    # print("-----")
    alt_text = img.get("alt")
    src = base_url + img.get("src")
    # print(f"Image URL: {src}")
    # print(f"Alt Text: {alt_text}")
    # print("-----")
    header_data.append({
        "src": src,
        "alt": alt_text
    })
    
with open("header_data.json", "w") as f:
    json.dump(header_data, f, indent=4)


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(URL)
    # Wait for the page to load
    page.wait_for_selector(".playlist")
    
    playlist = page.query_selector(".playlist")
    items = playlist.query_selector_all(".item")
    
    video_data = []
    
    for item in items:
        link = item.query_selector(".heading a")
        title_span = item.query_selector(".heading .title")
        
        if link and title_span:
            link_url = link.get_attribute("href")
            title = title_span.inner_text()
            video_id = link_url.split("v=")[1]
            video_data.append({
                "title": title,
                "video-id": video_id
            })
            
            # print(f"Title: {title}")
            # print(f"Link: {link_url}")

    # Close the browser
    browser.close()
    
with open("video_data.json", "w") as f:
    json.dump(video_data, f, indent=4)