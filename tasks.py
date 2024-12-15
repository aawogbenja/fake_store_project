from celery import Celery
from scraper.fetch_products import fetch_products

app = Celery('tasks', broker='redis://localhost:6379/0')

@app.task
def fetch_and_save():
    fetch_products()