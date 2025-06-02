from flask import Flask, render_template
from scraper import scrape_remote_jobs
app = Flask(__name__)

@app.route('/')
def index():
    jobs = scrape_remote_jobs()
    return render_template('index.html', jobs=jobs)

if __name__ == '__main__':
    app.run()