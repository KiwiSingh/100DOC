from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from time import time

options = Options()

# Keep Chrome open after the script exits
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=Service(), options=options)
wait = WebDriverWait(driver, 10)

driver.get("https://ozh.github.io/cookieclicker/")

# Bypass that devious language selector
try:
    ld = wait.until(EC.element_to_be_clickable((By.ID, "langSelect-EN")))
    ld.click()
except TimeoutException:
    print("Couldn't find the language selector, oomf!")

# Wait for the cookie to become available
try:
    wait.until(EC.element_to_be_clickable((By.ID, "bigCookie")))
except TimeoutException:
    print("Couldn't find the big cookie, oomf!")

# Get all store items (products 0-17)
item_ids = [f"product{i}" for i in range(18)]

def get_stats():
    """Safely get the current cookie count and cookies per second."""
    try:
        n_cookies = int(driver.find_element(By.ID, "cookies").text.split()[0].replace(",", ""))
        cps_text = driver.find_element(By.ID, "cookiesPerSecond").text
        cookies_per_second = cps_text.split("per second:")[1].strip().replace(",", "")
        return n_cookies, cookies_per_second
    except (NoSuchElementException, StaleElementReferenceException, ValueError, IndexError):
        return None, None

# Set timers
wait_time = 5
timeout = time() + wait_time  # Check for purchases every 5 seconds
five_min = time() + 300  # Run for 5 minutes

while True:
    # Re-find the cookie every click because Cookie Clicker likes to randomly rebuild its DOM
    try:
        driver.find_element(By.ID, "bigCookie").click()
    except StaleElementReferenceException:
        continue
    except NoSuchElementException:
        print("Couldn't find the big cookie, oomf!")
        continue

    if time() > timeout:
        n_cookies, cookies_per_second = get_stats()

        if n_cookies is None:
            print("Couldn't find cookie count or CPS, oomf!")
        else:
            # Find all available upgrades
            try:
                upgrades = driver.find_elements(By.CSS_SELECTOR, "div[id^='product']")

                # Find the most expensive upgrade we can make
                best_upgrade = None
                for upgrade in reversed(upgrades):
                    try:
                        if "enabled" in upgrade.get_attribute("class"):
                            best_upgrade = upgrade
                            break
                    except StaleElementReferenceException:
                        continue

                # Buy the best upgrade if found
                if best_upgrade:
                    try:
                        best_upgrade.click()
                    except StaleElementReferenceException:
                        pass
            except StaleElementReferenceException:
                print("Cookie Clicker rearranged the store, oomf!")

        # Reset the timer
        timeout = time() + wait_time

    # Stop our timer after 5 minutes
    if time() > five_min:
        # Try to get a fresh count if possible
        n_cookies, cookies_per_second = get_stats()

        if n_cookies is None:
            print("Couldn't get final cookie count.")
            n_cookies = "Unknown"
        if cookies_per_second is None:
            cookies_per_second = "Unknown"

        print(f"Final result: {n_cookies}\n")
        print(f"Your best rate was: {cookies_per_second}")
        break  # Always exit after 5 minutes

driver.quit()  # Don't wanna keep it open like a madman, innit?

# Yes, I had ChatGPT refactor this, because the constantly
# updating DOMs in Cookie Clicker were driving me insane
# when my code was fundamentally correct!!!