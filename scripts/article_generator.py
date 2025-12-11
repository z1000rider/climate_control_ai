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

if not topics:
    raise SystemExit("No topics found in data/topics.json")

topic = topics[0]  # first topic for now

def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")

slug = slugify(topic)
os.makedirs("data/articles", exist_ok=True)
output_path = f"data/articles/{slug}.md"

prompt = f"""
Write a detailed, helpful blog article in Markdown about:

\"{topic}\"

Niche: Smart climate control (thermostats, purifiers, humidifiers, AC units).
Explain benefits, use-cases, setup tips, and practical advice.
Use headings (##), bullet lists and short paragraphs.
Target length: about 1500–2000 words.
No affiliate links, just neutral content.
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}]
)

article = response.choices[0].message.content

with open(output_path, "w") as f:
    f.write(article)

print(f"Article for '{topic}' saved to {output_path}")
