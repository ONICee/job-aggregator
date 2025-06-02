from sources.remoteok import scrape_remoteok
# from sources.weworkremotely import scrape_wwr
# from sources.remotive import scrape_remotive

def scrape_remote_jobs():
    jobs = []
    jobs += scrape_remoteok()
    # jobs += scrape_wwr()
    # jobs += scrape_remotive()
    print(f"✅ Total aggregated: {len(jobs)} jobs.")
    return jobs
