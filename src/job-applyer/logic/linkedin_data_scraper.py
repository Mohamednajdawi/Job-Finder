import platform
import time

import undetected_chromedriver as uc
from bs4 import BeautifulSoup
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


def search_linkedin_data(profile_link):
    driver = get_chrome_driver()
    expected_url = profile_link + "?original_referer="
    driver.get(expected_url)

    # Wait until the current URL matches the expected URL
    while driver.current_url != expected_url:
        driver.get(expected_url)
        print("Trying to connect")
        print("now: ", driver.current_url)
        time.sleep(1)  # Sleep for 1 second before checking again

    # Wait for the button to be present and clickable
    try:
        dismiss_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.modal__dismiss"))
        )
        dismiss_button.click()
        print("Button clicked successfully")
    except:
        print("Error clicking the button")
