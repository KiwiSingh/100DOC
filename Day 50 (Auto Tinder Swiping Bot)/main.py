from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
    TimeoutException,
    WebDriverException,
)
import os
from time import sleep


# Chrome options
chrome_options = Options()

# Chrome binary location (mine lives
# on an external SSD)
chrome_options.binary_location = (
    "/Volumes/Zweidrive/Applications/Google Chrome.app/"
    "Contents/MacOS/Google Chrome"
)

# Use a dedicated Selenium Chrome profile
chrome_options.add_argument(
    "--user-data-dir=" +
    os.path.expanduser("~/selenium-chrome-profile")
)

chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--disable-blink-features=AutomationControlled")


# Start Chrome
driver = webdriver.Chrome(options=chrome_options)


# Login with stealth
# May be different between
# Windows and macOS
stealth(
    driver,
    languages=["en-US", "en"],
    vendor="Google Inc.",
    platform="MacIntel",
    webgl_vendor="Intel Inc.",
    renderer="Intel Iris OpenGL Engine",
    fix_hairline=True,
)


driver.get("https://www.tinder.com")

driver.maximize_window()

wait = WebDriverWait(driver, 15)


try:
    wait.until(EC.presence_of_element_located(
            (By.TAG_NAME, "body")
        )
    )

    # Look for the login button
    login_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[class*='c1p6lbu0']")))

    login_btn.click()

    print("Login button found and clicked.")

except WebDriverException:
    # We use a catch-all WebDriverException "except" block because Selenium can
    # behave weird sometimes, even when Tinder is logged in
    print("Already logged in, or login button was not found.")

# Unlike Angela's implementation, we're gonna manually dismiss
# everything, so that it stays cached in our Chrome profile.
# This also means manually dismissing most of the weird popups Tinder
# likes to randomly give. Idc, my script my rules.

# I'm using a while loop since I have Tinder Gold;
# feel free to change this to a for loop if you're
# a pleb with free Tinder.
while True:

    # Add a 1 second delay between likes.
    sleep(1)

    try:
        print("called")

        like_button = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    '//button[.//span[contains(@class, "Hidden") and text()="Like"]]'
                )
            )
        )

        like_button.click()

    # Catches the cases where there is a "Matched" pop-up
    # in front of the "Like" button:
    except ElementClickInterceptedException:
        try:
            match_popup = driver.find_element(
                By.CSS_SELECTOR,
                ".itsAMatch a"
            )
            match_popup.click()

        # Catches the cases where the match popup has not yet loaded.
        except NoSuchElementException:
            sleep(2)

    except TimeoutException:
        print("Like button did not load, retrying...")
        sleep(2)

    if driver.find_elements(By.XPATH, "//button[contains(., 'Go Global')]"):
        print("Whoa there buddy! You've run out of local women to match with.")
        break