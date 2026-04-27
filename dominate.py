import os, datetime, requests, time
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
AMAZON_TAG = os.environ.get("AMAZON_TAG")
if not GEMINI_KEY: raise ValueError("Missing GEMINI_API_KEY")
print(f"Starting with tag: {AMAZON_TAG}")
NICHES = ["best camping stove", "lightweight tent", "sleeping bag", "camping chair"]
topic = NICHES[datetime.datetime.now().timetuple().tm_yday % len(NICHES)]
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
resp = requests.post(url, headers={"Content-Type":"application/json"}, json={"contents":[{"parts":[{"text":f"Write 500-word review of {topic} for UK. Include Amazon link with tag {AMAZON_TAG}. Return HTML."}]}],"generationConfig":{"maxOutputTokens":1000}})
print(f"API status: {resp.status_code}")
if resp.status_code == 200:
    html = resp.json()["candidates"][0]["content"]["parts"][0]["text"]
    os.makedirs("posts", exist_ok=True)
    with open("posts/index.html", "w") as f: f.write(f"<html><body>{html}<footer>Amazon</footer></body></html>")
    with open("index.html", "w") as f: f.write("<h1>Camping UK</h1><a href='posts/index.html'>Latest</a>")
    print("Success!")
else:
    print(resp.text)
    exit(1)
