from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import pandas as pd


def get_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=options)


def build_url(role, location, start=0):
    role = role.replace(" ", "+")
    location = location.replace(" ", "+")
    return f"https://in.indeed.com/jobs?q={role}&l={location}&start={start}"


def extract_jobs_from_page(driver):
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "job_seen_beacon"))
    )

    job_cards = driver.find_elements(By.CLASS_NAME, "job_seen_beacon")
    jobs = []

    for card in job_cards:
        try:
            title = card.find_element(By.CLASS_NAME, "jobTitle").text
        except:
            title = None

        try:
            company = card.find_element(By.CLASS_NAME, "companyName").text
        except:
            company = None

        try:
            location = card.find_element(By.CLASS_NAME, "companyLocation").text
        except:
            location = None

        try:
            summary = card.find_element(By.CLASS_NAME, "job-snippet").text
        except:
            summary = None

        try:
            date = card.find_element(By.CLASS_NAME, "date").text
        except:
            date = None

        try:
            url = card.find_element(By.CLASS_NAME, "jcs-JobTitle").get_attribute("href")
        except:
            url = None

        jobs.append({
            "title": title,
            "company": company,
            "location": location,
            "summary": summary,
            "date_posted": date,
            "url": url
        })

    return jobs


def scrape_indeed(role="data analyst", location="remote", pages=3, delay=2):
    driver = get_driver()
    all_jobs = []

    for page in range(pages):
        start = page * 10
        url = build_url(role, location, start)
        print(f"Scraping: {url}")
        driver.get(url)
        time.sleep(delay)
        jobs = extract_jobs_from_page(driver)
        all_jobs.extend(jobs)

    driver.quit()
    return pd.DataFrame(all_jobs)
