import os, datetime, requests, time

GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
AMAZON_TAG = os.environ.get("AMAZON_TAG")
if not GEMINI_KEY:
    raise ValueError("Missing GEMINI_API_KEY")

SITE_URL = f"https://{os.environ['GITHUB_REPOSITORY_OWNER']}.github.io/{os.environ['GITHUB_REPOSITORY_NAME']}"

NICHES = ["best camping stove under 50", "lightweight tent", "sleeping bag 30 degree"]

def pick_topic():
    return NICHES[datetime.datetime.now().timetuple().tm_yday % len(NICHES)]

def generate_article(topic):
    prompt = f"Write 1000-word review of '{topic}' for UK. Include Amazon link: https://www.amazon.co.uk/s?k={topic.replace(' ','+')}&tag={AMAZON_TAG}. Return HTML."
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    resp = requests.post(url, headers={"Content-Type":"application/json"}, json={
        "contents":[{"parts":[{"text":prompt}]}],
        "generationConfig":{"temperature":0.7,"maxOutputTokens":1500}
    })
    resp.raise_for_status()
    return resp.json()["candidates"][0]["content"]["parts"][0]["text"]

def save_article(html, topic):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    slug = topic.lower().replace(" ","-")
    os.makedirs(today, exist_ok=True)
    with open(f"{today}/{slug}.html", "w") as f:
        f.write(f"<html><body>{html}<footer>Amazon Associate</footer></body></html>")

if __name__ == "__main__":
    for _ in range(3):
        t = pick_topic()
        html = generate_article(t)
        save_article(html, t)
        time.sleep(5)
    # Create index
    with open("index.html", "w") as f:
        f.write("<h1>Camping UK</h1><p>Daily deals</p>")
    print("Done")
