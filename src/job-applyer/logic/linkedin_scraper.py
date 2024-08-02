import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait


def search_linkedin_jobs(job_title, country):
    options = uc.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = uc.Chrome(options=options)

    number_job_listings = 0
    while number_job_listings == 0:
        driver.get(
            f"https://www.linkedin.com/jobs/search/?keywords={job_title}&location={country}"
        )
        # Wait for job listings to load
        WebDriverWait(driver, 10)
        # .until(EC.presence_of_element_located((By.CLASS_NAME, "two-pane-serp-page__detail-view")))
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        job_listings = soup.find_all("div", class_="base-search-card__info")
        number_job_listings = len(job_listings)
        print("Number of Founded Jobs: ", len(job_listings))

    jobs = []
    for job in job_listings[:3]:  # Limit to first 5 jobs
        title = job.find("h3", class_="base-search-card__title").text.strip()
        company = job.find("h4", class_="base-search-card__subtitle").text.strip()
        link = job.find("h4", class_="base-search-card__subtitle").find("a")["href"]
        jobs.append({"title": title, "company": company, "description": "", "link": link})
    return jobs