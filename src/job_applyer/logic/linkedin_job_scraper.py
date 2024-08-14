import platform
import time

import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
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


def wait_and_find_element(driver, by, value, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))
        return element
    except TimeoutException:
        print(f"Element not found: {value}")
        return None


def search_linkedin_jobs(job_title, country, number_of_jobs):
    driver = get_chrome_driver()
    number_job_listings = 0

    while number_job_listings < number_of_jobs:
        driver.get(f"https://www.linkedin.com/jobs/search/?keywords={job_title}&location={country}")
        time.sleep(5)  # Wait for page to load
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        job_listings = soup.find_all("div", class_="base-search-card__info")
        number_job_listings = len(job_listings)
        print("Number of Founded Jobs: ", number_job_listings)

    jobs = []
    for i, job in enumerate(job_listings[:number_of_jobs]):
        print("Working on job number: ", i + 1)
        title = job.find("h3", class_="base-search-card__title").text.strip()
        company = job.find("h4", class_="base-search-card__subtitle").text.strip()

        link_element = wait_and_find_element(driver, By.CLASS_NAME, "base-card__full-link")
        if link_element:
            link = link_element.get_attribute("href")
            driver.get(link)
            time.sleep(3)

            try:
                show_more_button = wait_and_find_element(
                    driver, By.CLASS_NAME, "show-more-less-html__button"
                )
                if show_more_button:
                    show_more_button.click()
                    time.sleep(3)
            except:
                pass

            description_element = wait_and_find_element(
                driver, By.CLASS_NAME, "show-more-less-html__markup"
            )
            description_text = (
                description_element.get_attribute("innerHTML") if description_element else ""
            )

            # location = driver.find_element(By.CSS_SELECTOR, "span.topcard__flavor--bullet").text
            # post_time = driver.find_element(By.CSS_SELECTOR, "span.posted-time-ago__text").text
            # applicants = driver.find_element(By.CSS_SELECTOR, "span.num-applicants__caption").text
            try:
                location = wait_and_find_element(
                    driver, By.CSS_SELECTOR, "span.topcard__flavor--bullet"
                ).text
            except:
                location = ""
            try:
                post_time = wait_and_find_element(
                    driver, By.CSS_SELECTOR, "span.posted-time-ago__text"
                ).text
            except:
                post_time = ""
            try:
                applicants = wait_and_find_element(
                    driver, By.CSS_SELECTOR, "span.num-applicants__caption"
                ).text
            except:
                applicants = "Over 100 Applicants"
            jobs.append(
                {
                    "title": title,
                    "company": company,
                    "description": description_text,
                    "link": link,
                    "location": location,
                    "post_time": post_time,
                    "applicants": applicants,
                }
            )

    driver.quit()
    return jobs
