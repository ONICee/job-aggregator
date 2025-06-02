import requests
from bs4 import BeautifulSoup

def categorize_job(title):
    title = title.lower()
    if "frontend" in title or "front-end" in title:
        return "Frontend"
    elif "backend" in title or "back-end" in title:
        return "Backend"
    elif "fullstack" in title or "full-stack" in title:
        return "Fullstack"
    elif "mobile" in title or "android" in title or "ios" in title:
        return "Mobile"
    elif "devops" in title or "infrastructure" in title:
        return "DevOps"
    elif "data" in title or "ml" in title or "ai" in title:
        return "Data"
    else:
        return "Other"

def scrape_remote_jobs():
    url = "https://remoteok.com/remote-dev-jobs"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        jobs = []

        listings = soup.find_all("tr", class_="job")
        if not listings:
            print("⚠️ No job listings found.")
        for job in listings:
            try:
                title = job.find("h2").get_text(strip=True)
                company = job.find("h3").get_text(strip=True)
                link = "https://remoteok.com" + job['data-href']
                category = categorize_job(title)

                description = job.find("td", class_="company_and_position").get_text(strip=True)[:150] + "..."
                date_posted = job.find("time")
                posted = date_posted['datetime'] if date_posted else "N/A"

                jobs.append({
                    "title": title,
                    "company": company,
                    "link": link,
                    "category": category,
                    "description": description,
                    "date_posted": posted
                })
            except Exception as e:
                print("⚠️ Error processing job:", e)

        print(f"✅ Scraped {len(jobs)} jobs.")
        return jobs
    except Exception as e:
        print("❌ Scraping failed:", e)
        return []
