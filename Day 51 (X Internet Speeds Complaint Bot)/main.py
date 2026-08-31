from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import os

PROMISED_DOWN = 100
PROMISED_UP = 100
ISP = "@airtelindia @Airtel_Presence"


class InternetSpeedTwitterBot():

    def __init__(self):

        # Chrome options
        chrome_options = Options()

        # Chrome binary location (mine lives
        # on an external SSD)
        chrome_options.binary_location = (
            "/Volumes/Zweidrive/Applications/Google Chrome.app/"
            "Contents/MacOS/Google Chrome"
        )

        # Use a dedicated Selenium Chrome profile
        chrome_options.add_argument("--user-data-dir=" + os.path.expanduser("~/selenium-chrome-profile"))
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")

        # Start Chrome
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 20)

        # Login with stealth
        # May be different between
        # Windows and macOS
        stealth(self.driver, languages=["en-US", "en"], vendor="Google Inc.", platform="MacIntel", webgl_vendor="Intel Inc.", renderer="Intel Iris OpenGL Engine", fix_hairline=True)

        self.up = 0
        self.down = 0

    def get_internet_speed(self):

        self.driver.get("https://www.speedtest.net/")
        sleep(3)

        start_button = self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/div/div[2]/div[2]/div[2]/div/div/div[2]/div[2]/button')
        start_button.click()

        sleep(60)

        self.down = float(self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/div/div[2]/div[2]/div[2]/div/div/div/div[2]/div[2]/div[1]/div[1]/div/h3').text)
        self.up = float(self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/div/div[2]/div[2]/div[2]/div/div/div/div[2]/div[2]/div[1]/div[2]/div/h3').text)

        return self.down, self.up

    def tweet_at_provider(self):

        self.driver.get("https://x.com")

        # Wait for user to login; X's login flow is extremely broken and held together with duct tape.
        # Trying to automate the login flow only results in account
        # restrictions.
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div')))
        except NoSuchElementException:
            sleep(60)

        # Send tweet
        tweet = f"Hey {ISP}, why is my internet speed {self.down} down/{self.up} up - when I pay for {PROMISED_DOWN} down/{PROMISED_UP} up?"

        self.tweet_input = self.driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div/div')
        self.tweet_input.click()
        self.tweet_input.send_keys(tweet)

        self.post_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div/div/div[3]/button/div/div/span/span')))
        self.post_button.click()


# Initialize the bot
bot = InternetSpeedTwitterBot()

# Get internet speed
bot.get_internet_speed()

# Yell at provider on X
if bot.down < PROMISED_DOWN or bot.up < PROMISED_UP:
    bot.tweet_at_provider()