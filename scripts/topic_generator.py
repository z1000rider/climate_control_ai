import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

prompt = """
Generate 20 long-tail content ideas for the niche: Smart Climate Control.
Focus on smart thermostats, humidifiers, air purifiers, dehumidifiers, and smart AC units.
Return only the list, no explanations.
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}]
)

ideas_text = response.choices[0].message.content
ideas = [line.strip("0123456789. ").strip() for line in ideas_text.split("\n") if line.strip()]

# Save to data/topics.json
os.makedirs("data", exist_ok=True)
with open("data/topics.json", "w") as f:
    json.dump(ideas, f, indent=2)

print("Saved", len(ideas), "topics to data/topics.json")
