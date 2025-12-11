import os
import json
import re
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load topics
with open("data/topics.json", "r") as f:
    topics = json.load(f)

def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")

os.makedirs("data/articles", exist_ok=True)

# How many articles to create in one run
MAX_ARTICLES = 5

created = 0
for topic in topics:
    if created >= MAX_ARTICLES:
        break

    slug = slugify(topic)
    output_path = f"data/articles/{slug}.md"

    # skip if already exists
    if os.path.exists(output_path):
        print(f"Skipping existing article: {output_path}")
        continue

    prompt = f"""
    Write a detailed, helpful blog article in Markdown about:

    \"{topic}\"

    Niche: Smart climate control (thermostats, purifiers, humidifiers, AC units).
    Explain benefits, use-cases, setup tips, and practical advice.
    Use headings (##), bullet lists and short paragraphs.
    Target length: about 1500–2000 words.
    No affiliate links, just neutral content.
    """

    print(f"Generating article for: {topic}")
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    article = response.choices[0].message.content

    with open(output_path, "w") as f:
        f.write(article)

    print(f"Saved to {output_path}\n")
    created += 1

print(f"Done. Created {created} new articles.")
