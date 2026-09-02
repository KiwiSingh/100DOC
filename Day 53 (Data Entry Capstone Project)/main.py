import requests
import bs4
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdDPreHD6-mV6f2hRPhkgx3kN3sXn2IX99XyYDvvvXzaTgBew/viewform"
FAKE_ZILLOW = "https://appbrewery.github.io/Zillow-Clone/"
def get_property_attrs():
# Get property links, addresses, and prices from the fake Zillow website
    header = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
    }

    response = requests.get(FAKE_ZILLOW, headers=header)
    response.raise_for_status()
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    property_link_elements = soup.select(".StyledPropertyCardDataWrapper a")
    property_links = [link.get("href") for link in property_link_elements]
    print(f"There are {len(property_links)} property links in total.")
    print(property_links)

    property_address_elements = soup.select(".StyledPropertyCardDataWrapper address")
    property_addresses = [address.get_text().replace(" | ", " ").strip() for address in property_address_elements]

    print(f"\n After having been cleaned up, the {len(property_addresses)} addresses now look like this: \n")
    print(property_addresses)

    property_price_elements = soup.select(".PropertyCardWrapper span")
    property_prices = [price.get_text().replace("/mo", "").split("+")[0] for price in property_price_elements if "$" in price.text]
    print(f"\n After having been cleaned up, the {len(property_prices)} prices now look like this: \n")
    print(property_prices)

    properties = [
        {
            "Address": address,
            "Price": price,
            "Link": link
        }
        for address, price, link in zip(property_addresses, property_prices, property_links)
    ]
    return properties

properties = get_property_attrs()

def fill_out_form():
# Fill out the Google Form with the property data
    # Chrome options
    chrome_options = Options()

    # Chrome binary location (mine lives on an external SSD)
    chrome_options.binary_location = (
        "/Volumes/Zweidrive/Applications/Google Chrome.app/"
        "Contents/MacOS/Google Chrome"
    )

    # Use a dedicated Selenium Chrome profile
    chrome_options.add_argument(
        "--user-data-dir=" + os.path.expanduser("~/selenium-chrome-profile")
    )
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    # Start Chrome
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 20)

    # Use stealth
    # May be different between Windows and macOS
    stealth(
        driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="MacIntel",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True
    )


    for property in properties:
        driver.get(FORM_URL)

        address_field = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input'))
        )
        price_field = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
        link_field = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')

        address_field.send_keys(property["Address"])
        price_field.send_keys(property["Price"])
        link_field.send_keys(property["Link"])

        driver.find_element(By.XPATH, "//span[text()='Submit']").click()

        sleep(2)
fill_out_form()