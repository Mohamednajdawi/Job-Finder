import platform
import time

import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


def get_chrome_driver():
    options = uc.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    if platform.system() == "Linux" and platform.machine() == "aarch64":
        return uc.Chrome(
            options=options,
            use_subprocess=True,
            headless=True,
            driver_executable_path="/usr/bin/chromedriver",
        )
    else:
        return uc.Chrome(options=options)


def search_linkedin_jobs(job_title, country):
    driver = get_chrome_driver()
    number_job_listings = 0

    while number_job_listings == 0:
        driver.get(f"https://www.linkedin.com/jobs/search/?keywords={job_title}&location={country}")
        WebDriverWait(driver, 10)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        job_listings = soup.find_all("div", class_="base-search-card__info")
        number_job_listings = len(job_listings)
        print("Number of Founded Jobs: ", number_job_listings)

    jobs = []
    for i, job in enumerate(job_listings[:1]):  # Limit to first 3 jobs
        print("Working on job number: ", i + 1)
        title = job.find("h3", class_="base-search-card__title").text.strip()
        company = job.find("h4", class_="base-search-card__subtitle").text.strip()
        link_element = driver.find_element(By.CLASS_NAME, "base-card__full-link")
        link = link_element.get_attribute("href")
        driver.get(link)
        time.sleep(7)

        try:
            show_more_button = driver.find_element(By.CLASS_NAME, "show-more-less-html__button")
            show_more_button.click()
            time.sleep(7)
        except:
            pass  # Button might not be present for all job listings

        description_element = driver.find_element(By.CLASS_NAME, "show-more-less-html__markup")
        description_text = description_element.get_attribute("innerHTML")
        jobs.append(
            {"title": title, "company": company, "description": description_text, "link": link}
        )

    driver.quit()
    return jobs
