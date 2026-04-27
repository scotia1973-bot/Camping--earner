import os, datetime, requests, time

OPENROUTER_KEY = os.environ.get("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")
AMAZON_TAG = os.environ.get("gadgethumans-21")

if not OPENROUTER_KEY:
    raise ValueError("Missing OPENROUTER_API_KEY secret")

NICHES = ["best camping stove under 50", "lightweight tent for backpacking", "sleeping bag 30 degree", "camping chair for bad back", "water filter for hiking", "headlamp with red light", "power bank for camping", "camping cookware set nonstick"]

def pick_topic():
    return NICHES[datetime.datetime.now().timetuple().tm_yday % len(NICHES)]

def generate_article(topic):
    prompt = f"""Write a 1000-word review of '{topic}' for UK Amazon shoppers. 
    Include this link: https://www.amazon.co.uk/s?k={topic.replace(' ', '+')}&tag={AMAZON_TAG}
    Return HTML. Write conversationally, like a human expert."""
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "meta-llama/llama-3-8b-instruct:free",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 2000,
        "temperature": 0.7
    }
    response = requests.post(url, json=payload, headers=headers, timeout=60)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

def save_article(html, topic):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    slug = topic.lower().replace(" ", "-").replace(",", "")
    os.makedirs(today, exist_ok=True)
    with open(f"{today}/{slug}.html", "w") as f:
        f.write(f"<html><body><h1>{topic}</h1>{html}<footer>As an Amazon Associate I earn from qualifying purchases.</footer></body></html>")

if __name__ == "__main__":
    for i in range(3):
        t = pick_topic()
        print(f"Generating {i+1}/3: {t}")
        html = generate_article(t)
        save_article(html, t)
        time.sleep(10)
    
    with open("index.html", "w") as f:
        f.write("<h1>Camping Gear UK</h1><p>Daily honest reviews of budget camping gear</p>")
    
    print("Success! 3 articles published.")
