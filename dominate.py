import os, datetime, requests, time

GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
AMAZON_TAG = os.environ.get("AMAZON_TAG")

if not GEMINI_KEY:
    raise ValueError("Missing GEMINI_API_KEY secret")

print(f"API Key found. Amazon tag: {AMAZON_TAG}")

NICHES = ["best camping stove under 50", "lightweight tent for backpacking", "sleeping bag 30 degree", "camping chair for bad back", "water filter for hiking", "headlamp with red light", "power bank for camping", "camping cookware set nonstick"]

topic = NICHES[datetime.datetime.now().timetuple().tm_yday % len(NICHES)]
print(f"Generating: {topic}")

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
prompt = f"Write a 1000-word review of '{topic}' for UK audience. Include Amazon UK link: https://www.amazon.co.uk/s?k={topic.replace(' ', '+')}&tag={AMAZON_TAG}. Return HTML."

response = requests.post(url, headers={"Content-Type": "application/json"}, json={
    "contents": [{"parts": [{"text": prompt}]}],
    "generationConfig": {"temperature": 0.7, "maxOutputTokens": 1500}
})

print(f"API status: {response.status_code}")

if response.status_code == 200:
    result = response.json()
    html = result["candidates"][0]["content"]["parts"][0]["text"]
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    os.makedirs(today, exist_ok=True)
    with open(f"{today}/index.html", "w") as f:
        f.write(f"<html><body><h1>{topic}</h1>{html}<footer>Amazon Associate</footer></body></html>")
    with open("index.html", "w") as f:
        f.write(f"<html><body><h1>Camping UK</h1><p>Latest: {topic}</p><a href='{today}/index.html'>Read more</a></body></html>")
    print("Success!")
else:
    print(f"Error: {response.text}")
    raise Exception("API call failed")
