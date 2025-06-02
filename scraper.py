import requests
from bs4 import BeautifulSoup

def detect_category(title):
    title = title.lower()
    if any(keyword in title for keyword in ["frontend", "react", "vue", "angular"]):
        return "Frontend"
    elif any(keyword in title for keyword in ["backend", "node", "django", "rails", "php"]):
        return "Backend"
    elif "fullstack" in title or ("frontend" in title and "backend" in title):
        return "Fullstack"
    elif any(keyword in title for keyword in ["android", "ios", "flutter", "mobile"]):
        return "Mobile"
    elif any(keyword in title for keyword in ["devops", "infrastructure", "aws", "kubernetes", "docker"]):
        return "DevOps"
    elif any(keyword in title for keyword in ["data", "machine learning", "ml", "ai", "analyst", "python"]):
        return "Data"
    else:
        return "Other"

def scrape_remoteok():
    url = "https://remoteok.com/remote-dev-jobs"
    headers = {"User-Agent": "Mozilla/5.0"}
    jobs = []

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        listings = soup.find_all("tr", class_="job")

        for job in listings:
            try:
                title = job.find("h2").get_text(strip=True)
                company = job.find("h3").get_text(strip=True)
                link = "https://remoteok.com" + job['data-href']
                category = detect_category(title)
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
            except:
                continue

    except Exception as e:
        print("❌ RemoteOK scraping failed:", e)

    return jobs

def scrape_weworkremotely():
    url = "https://weworkremotely.com/categories/remote-programming-jobs"
    jobs = []

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        listings = soup.select("section.jobs li.feature")

        for job in listings:
            try:
                link_tag = job.find("a", href=True)
                if not link_tag:
                    continue

                link = "https://weworkremotely.com" + link_tag["href"]
                company = job.find("span", class_="company").get_text(strip=True)
                title = job.find("span", class_="title").get_text(strip=True)
                category = detect_category(title)
                posted = "N/A"
                description = f"{company} is hiring for {title}."

                jobs.append({
                    "title": title,
                    "company": company,
                    "link": link,
                    "category": category,
                    "description": description,
                    "date_posted": posted
                })
            except:
                continue

    except Exception as e:
        print("❌ WeWorkRemotely scraping failed:", e)

    return jobs

def scrape_remotive():
    url = "https://remotive.io/api/remote-jobs?category=software-dev"
    jobs = []

    try:
        response = requests.get(url)
        data = response.json()

        for job in data["jobs"]:
            title = job["title"]
            category = detect_category(title)

            jobs.append({
                "title": title,
                "company": job["company_name"],
                "link": job["url"],
                "category": category,
                "description": job["description"][:150] + "...",
                "date_posted": job["publication_date"].split("T")[0]
            })

    except Exception as e:
        print("❌ Remotive scraping failed:", e)

    return jobs

def scrape_remote_jobs():
    jobs = []
    jobs += scrape_remoteok()
    jobs += scrape_weworkremotely()
    jobs += scrape_remotive()

    print(f"✅ Total jobs scraped: {len(jobs)}")
    return jobs
