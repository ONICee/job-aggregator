import requests
from bs4 import BeautifulSoup

def scrape_remoteok():
    url = "https://remoteok.com/remote-dev-jobs"
    headers = {"User-Agent": "Mozilla/5.0"}
    jobs = []

    try:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        listings = soup.find_all("tr", class_="job")

        for job in listings:
            try:
                title = job.find("h2").get_text(strip=True)
                company = job.find("h3").get_text(strip=True)
                link = "https://remoteok.com" + job['data-href']
                tags = [tag.get_text(strip=True).lower() for tag in job.find_all("div", class_="tag")]
                category = categorize(tags)
                desc = job.find("td", class_="company_and_position").get_text(strip=True)[:150] + "..."
                date_posted = job.find("time")
                posted = date_posted['datetime'] if date_posted else "N/A"

                jobs.append({
                    "title": title, "company": company, "link": link,
                    "category": category, "description": desc, "date_posted": posted
                })
            except:
                continue
    except Exception as e:
        print("❌ RemoteOK error:", e)

    return jobs

def categorize(tags):
    categories = {
        "frontend": ["frontend", "javascript", "react"],
        "backend": ["backend", "node", "django"],
        "fullstack": ["fullstack"],
        "mobile": ["android", "ios", "flutter"],
        "devops": ["devops", "cloud", "aws", "docker"],
        "data": ["data", "ml", "ai", "analytics"]
    }

    for key, keywords in categories.items():
        if any(kw in tags for kw in keywords):
            return key.capitalize()
    return "Other"
