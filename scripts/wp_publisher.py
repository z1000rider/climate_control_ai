import os
import base64
import json
import requests
from dotenv import load_dotenv

load_dotenv()

WP_URL = os.getenv("WORDPRESS_URL")  # e.g. https://climatehomehub.wordpress.com
WP_USER = os.getenv("WORDPRESS_USER")
WP_APP_PASSWORD = os.getenv("WORDPRESS_APP_PASSWORD")

# Extract just the domain part for WordPress.com API
site_domain = WP_URL.replace("https://", "").replace("http://", "").strip("/")

API_URL = f"https://public-api.wordpress.com/wp/v2/sites/{site_domain}/posts"


auth_str = f"{WP_USER}:{WP_APP_PASSWORD}"
auth_header = base64.b64encode(auth_str.encode()).decode()

headers = {
    "Authorization": f"Basic {auth_header}",
    "Content-Type": "application/json"
}

# pick one article file
articles_dir = "data/articles"
files = [f for f in os.listdir(articles_dir) if f.endswith(".md")]
if not files:
    raise SystemExit("No articles found in data/articles")

file_name = files[0]
with open(os.path.join(articles_dir, file_name), "r") as f:
    content = f.read()

title = file_name.replace("-", " ").replace(".md", "").title()

payload = {
    "title": title,
    "content": content,
    "status": "draft"   # later change to "publish" for auto-post
}

resp = requests.post(API_URL, headers=headers, data=json.dumps(payload))

print("Status:", resp.status_code)
print("Response:", resp.text[:500])
