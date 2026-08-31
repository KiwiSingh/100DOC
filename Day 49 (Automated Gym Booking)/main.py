from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import NoSuchElementException, TimeoutException

ACCOUNT_EMAIL = "kiwisingh@proton.me"
ACCOUNT_PASSWORD = "r4z0rr4z4h"
GYM_URL = "https://appbrewery.github.io/gym/"

profile_path = "/Users/parthasarathi/Library/Application Support/Firefox/SeleniumGym"

firefox_options = Options()
# Point directly to the persistent profile directory
firefox_options.add_argument("-profile")
firefox_options.add_argument(profile_path)
firefox_options.set_preference("detach", True)

driver = webdriver.Firefox(options=firefox_options)
driver.get(GYM_URL)
wait = WebDriverWait(driver, 5)

# Simple retry wrapper
def retry(func, retries=7, description=None):
    for i in range(retries):
        print(f"Trying {description}. Attempt: {i + 1}")
        try:
            return func()
        except TimeoutException, NoSuchElementException:
            if i == retries - 1:
                raise
            time.sleep(1)

def login():
    # Wait for login button to appear
    lb = wait.until(EC.element_to_be_clickable((By.ID, "login-button")))
    lb.click()

    # Login
    user_email = wait.until(EC.presence_of_element_located((By.ID, "email-input")))
    user_email.clear()
    user_email.send_keys(ACCOUNT_EMAIL)

    upass = driver.find_element(By.ID, "password-input")
    upass.clear()
    upass.send_keys(ACCOUNT_PASSWORD)

    sb = driver.find_element(By.ID, "submit-button")
    sb.click()

    wait.until(EC.presence_of_element_located((By.ID, "schedule-page")))

retry(login, description="login")

# Find all class cards
class_cards = driver.find_elements(By.CSS_SELECTOR, "div[id^='class-card-']")

booked_count = 0
waitlist_count = 0
already_booked_count = 0

processed_classes = []

for card in class_cards:
    day_group = card.find_element(By.XPATH, "./ancestor::div[contains(@id, 'day-group-')]")
    day_title = day_group.find_element(By.TAG_NAME, "h2").text

    if "Tue" in day_title or "Thu" in day_title:
        time_text = card.find_element(By.CSS_SELECTOR, "p[id^='class-time-']").text
        if "6:00 PM" in time_text:
            class_name = card.find_element(By.CSS_SELECTOR, "h3[id^='class-name-']").text
            book_button = card.find_element(By.CSS_SELECTOR, "button[id^='book-button-']")

            class_info = f"{class_name} on {day_title}"

            # Check if already booked
            if book_button.text == "Booked":
                print(f"✓ Already booked: {class_name} on {day_title}")
                already_booked_count+=1
                processed_classes.append(f"[Booked] {class_info}")
            elif book_button.text == "Waitlisted":
                print(f"✓ Already on waitlist: {class_name} on {day_title}")
                waitlist_count+=1
                processed_classes.append(f"[Waitlisted] {class_info}")
            elif book_button.text == "Book Class":
                # Book the class
                book_button.click()
                print(f"✓ Successfully booked: {class_name} on {day_title}")
                booked_count+=1
                processed_classes.append(f"[New Booking] {class_info}")
                time.sleep(1)
            elif book_button.text == "Join Waitlist":
                # Join waitlist if class is full
                book_button.click()
                print(f"✓ Joined waitlist for: {class_name} on {day_title}")
                waitlist_count+=1
                processed_classes.append(f"[New Waitlist] {class_info}")
                time.sleep(1)

# Verify bookings
total_booked = already_booked_count + booked_count + waitlist_count
print(f"\n--- Total Tuesday/Thursday 6pm classes: {total_booked} ---")

def get_my_bookings():
    print("\n--- VERIFYING ON MY BOOKINGS PAGE ---")
    mb_button = driver.find_element(By.XPATH, value='//*[@id="my-bookings-link"]')
    mb_button.click()

    # Wait for My Bookings page to load
    wait.until(EC.presence_of_element_located((By.ID, "my-bookings-page")))
    vbc = 0

    # Find ALL booking cards (both confirmed and waitlist)
    all_booking_cards = driver.find_elements(By.CSS_SELECTOR, "div[id*='card-']")

    for bc in all_booking_cards:
        when_para = bc.find_element(By.XPATH, value="/html/body/div/main/div/div[1]/div/div/div/p[1]")
        when_text = when_para.text
        # Check if it's a Tuesday or Thursday 6pm class
        if ("Tue" in when_text or "Thu" in when_text) and "6:00 PM" in when_text:
            class_name = bc.find_element(By.TAG_NAME, "h3").text
            print(f"  ✓ Verified: {class_name}")
            vbc += 1
        # Simple comparison
    print(f"\n--- VERIFICATION RESULT ---")
    print(f"Expected: {total_booked} bookings")
    print(f"Found: {vbc} bookings")

    if total_booked == vbc:
        print("✅ SUCCESS: All bookings verified!")
    else:
        print(f"❌ MISMATCH: Missing {total_booked - vbc} bookings")

    # Print a summary at the end
    print("\n--- BOOKING SUMMARY ---")
    print(f"Classes booked: {booked_count}")
    print(f"Waitlists joined: {waitlist_count}")
    print(f"Already booked/waitlisted: {already_booked_count}")
    print(f"Total 6pm classes processed: {booked_count + waitlist_count + already_booked_count}")

    # Print detailed class list
    print("\n--- DETAILED CLASS LIST ---")
    for class_detail in processed_classes:
        print(f"  • {class_detail}")

retry(get_my_bookings, description=get_my_bookings)



# Keep Firefox alive for five minutes (for no good reason)
time.sleep(300)

driver.quit()