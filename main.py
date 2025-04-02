import json

import bs4
import requests

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
    print(f"Image URL: {src}")
    print(f"Alt Text: {alt_text}")
    print("-----")
    header_data.append({
        "src": src,
        "alt": alt_text
    })
    
with open("header_data.json", "w") as f:
    json.dump(header_data, f, indent=4)
