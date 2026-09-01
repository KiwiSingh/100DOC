import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, TimeoutException
from time import sleep
from selenium.webdriver.common.keys import Keys
from random import uniform

SIMILAR_ACCOUNT = os.getenv("TARGET_ACCOUNT")
USERNAME = os.getenv("IG_USER") # This is a burner account of mine btw;
                                # don't use your real account lol
PASSWORD = os.getenv("IG_PASS")

class InstaFollower:

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

        # Use stealth
        # May be different between
        # Windows and macOS
        stealth(self.driver, languages=["en-US", "en"], vendor="Google Inc.", platform="MacIntel", webgl_vendor="Intel Inc.", renderer="Intel Iris OpenGL Engine", fix_hairline=True)

        self.driver.get("https://www.instagram.com/accounts/login/")

    def login(self):

        sleep(3)

        try:
            uname = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
            uname.send_keys(USERNAME)

            password = self.wait.until(EC.presence_of_element_located((By.NAME, "password")))
            password.send_keys(PASSWORD, Keys.ENTER)

        except TimeoutException:
            print("Already logged in, foo!")

        finally:
            sleep(30)  # Wait for user to enter 2FA code and dismiss all prompts

            try:
                save_info = self.driver.find_element(By.XPATH, "//button[normalize-space()='Not now']")
                save_info.click()
            except NoSuchElementException:
                print("We already did that, cuh!")

    def find_followers(self):
        sleep(5)

        # Open up the page for the target account
        self.driver.get(f"https://www.instagram.com/{SIMILAR_ACCOUNT}/")
        sleep(5)

        # Wait for followers button to load and clicks on it
        followers_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[.//span[contains(., 'followers')]]")))

        followers_button.click()
        sleep(2)

        # Wait for followers popup
        self.popup = self.driver.execute_script("""
            const divs = [...document.querySelectorAll('div')];

            return divs.find(div => {
                const style = getComputedStyle(div);
                return (
                    div.scrollHeight > div.clientHeight &&
                    div.clientHeight > 200 &&
                    style.overflowY !== 'visible'
                );
            });
            """)

        if not self.popup:
            raise RuntimeError("Couldn't find the followers popup.")

        print("Followers popup found.")

    def follow(self):
        last_scroll_height = 0
        stagnant_scrolls = 0
        follows = 0

        # Find "Follow" buttons
        while stagnant_scrolls < 3:
            buttons = self.driver.find_elements(By.XPATH, "//div[@role='dialog']//button[normalize-space()='Follow']")

            for button in buttons:
                try:
                    if button.is_displayed() and button.is_enabled():
                        button.click()
                        follows += 1

                        # Add rate limiting
                        sleep(uniform(2.5, 5.0))

                        try:
                            # Safety valve so that we don't unfollow people
                            # on accident lol
                            cancel = WebDriverWait(self.driver, 1).until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Cancel']")))
                            cancel.click()
                        except TimeoutException:
                            pass

                        if follows % 10 == 0:
                            sleep(uniform(15, 30))

                except ElementClickInterceptedException:
                    pass

            self.driver.execute_script(
                "arguments[0].scrollTop += arguments[0].clientHeight;",
                self.popup
            )

            sleep(uniform(2, 4))

            scroll_height = self.driver.execute_script(
                "return arguments[0].scrollHeight;",
                self.popup
            )

            if scroll_height == last_scroll_height:
                stagnant_scrolls += 1
            else:
                stagnant_scrolls = 0

            last_scroll_height = scroll_height

        print(f"Done. Followed {follows} accounts.")

bot = InstaFollower()
bot.login()
bot.find_followers()
bot.follow()