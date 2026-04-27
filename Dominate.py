import os, datetime, requests, time
GEMINI_KEY = os.environ["GEMINI_API_KEY"]
AMAZON_TAG = os.environ["AMAZON_TAG"]
SITE_URL = f"https://{os.environ['GITHUB_REPOSITORY_OWNER']}.github.io/{os.environ['GITHUB_REPOSITORY_NAME']}"
NICHES = ["best tent for heavy rain uk","camping coffee maker portable","insulated water bottle 40oz","camping air mattress queen","solar charger for devices","camping hatchet axe","camping lantern rechargeable","camping first aid kit comprehensive","camping stove propane","camping cooler rotomolded","camping folding table","camping hammock with bug net","camping saw folding","camping shovel survival","camping tarp waterproof","camping cot for adults","camping pillow compressible","camping towels quick dry","camping rug for tent","camping shower portable","camping toilet bucket","camping chair double","camping oven for stove","camping kettle stainless","camping spice rack","camping french press","camping marshmallow roaster","camping pizza oven","camping waffle maker","camping blender battery","camping electric cooler","camping fan rechargeable","camping heater propane","camping mosquito repellent","camping bear spray","camping knife sharpener","camping rope 550 paracord","camping carabiners","camping backpack 50L","camping gaiters","camping gaiters waterproof","camping bandana microfiber","camping hat sun protection","camping gloves","camping socks merino wool","camping underwear quick dry","camping rain suit","camping poncho","camping boot dryer"]
def pick_topic(): return NICHES[datetime.datetime.now().timetuple().tm_yday % len(NICHES)]
def generate_article(topic):
    prompt = f"Write 2000-word SEO review of '{topic}' for UK. Use Amazon UK links with tag={AMAZON_TAG}. Return HTML."
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    resp = requests.post(url, headers={"Content-Type":"application/json"}, json={"contents":[{"parts":[{"text":prompt}]}],"generationConfig":{"temperature":0.8,"maxOutputTokens":3000}})
    return resp.json()["candidates"][0]["content"]["parts"][0]["text"]
def create_html(html, topic):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    slug = topic.lower().replace(" ","-")[:50]
    os.makedirs(today, exist_ok=True)
    with open(f"{today}/{slug}.html", "w") as f:
        f.write(f"<!DOCTYPE html><html><head><title>{topic}</title></head><body><article>{html}</article><footer>As an Amazon Associate I earn.</footer></body></html>")
def update_index():
    items = []
    for root, dirs, files in os.walk("."):
        for f in files:
            if f.endswith(".html") and root != ".":
                items.append(f"<li><a href='{SITE_URL}/{root}/{f}'>{f}</a></li>")
    with open("index.html", "w") as f:
        f.write(f"<h1>Camping Insider UK</h1><ul>{''.join(items)}</ul>")
def create_sitemap():
    urls = []
    for root, dirs, files in os.walk("."):
        for f in files:
            if f.endswith(".html") and root != ".":
                urls.append(f"<url><loc>{SITE_URL}/{root}/{f}</loc></url>")
    with open("sitemap.xml", "w") as f:
        f.write(f"<?xml version='1.0'?><urlset xmlns='http://www.sitemaps.org/schemas/sitemap/0.9'>{''.join(urls)}</urlset>")
def ping_google(): requests.get(f"https://www.google.com/ping?sitemap={SITE_URL}/sitemap.xml", timeout=5)
def backlink():
    t = os.environ.get("GITHUB_TOKEN")
    if t:
        requests.post("https://api.github.com/gists", headers={"Authorization": f"token {t}"}, json={"public":True,"files":{"l.md":{"content":"# Deal\n[Click]("+SITE_URL+")"}}})
if __name__=="__main__":
    for _ in range(3): t=pick_topic(); create_html(generate_article(t), t); time.sleep(10)
    update_index(); create_sitemap(); ping_google(); backlink()
