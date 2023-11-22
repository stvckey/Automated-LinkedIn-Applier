from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
import time

# Gathering user info
email = input("Please enter your LinkedIn email: ")
password = input("Please enter your password: ")
job_title = input("Please enter the job title you're looking for (Ex: Software Engineer): ")

# Keep chrome open after opening the driver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.linkedin.com/")

# Setting up action chains
action = ActionChains(driver)

# Function to abort application process
def abort_application():
    # Click Close Button
    close_button = driver.find_element(by=By.CLASS_NAME, value="artdeco-modal__dismiss")
    close_button.click()

    time.sleep(2)
    # Click Discard Button
    discard_button = driver.find_elements(by=By.CLASS_NAME, value="artdeco-modal__confirm-dialog-btn")[1]
    discard_button.click()
    print("Done!")


# Filling out the forms
driver.find_element(By.ID, value="session_key").send_keys(email)
driver.find_element(By.ID, value="session_password").send_keys(password)

# Pressing the submit button
signin_button = driver.find_element(By.XPATH, value="//*[@id='main-content']/section[1]/div/div/form/div[2]/button")
signin_button.click()
input("Press 'ENTER' When the puzzle is complete!")

# Navigating to the 'jobs' page
jobs_button = driver.find_element(By.XPATH, value="//*[@id='global-nav']/div/nav/ul/li[3]/a")
jobs_button.click()

# Wait a second for the page to load...
time.sleep(3)

# Entering job search requirements
job_search = driver.find_element(By.CLASS_NAME, value="jobs-search-box__text-input")
job_search.send_keys(job_title)
job_search.send_keys(Keys.ENTER)

# Finding Easy Apply Button
time.sleep(3)
easy_apply = driver.find_element(By.XPATH, value="//*[text()='Easy Apply']")
easy_apply.click()
time.sleep(3)

# Iterating through the listings and applying
all_listings = driver.find_elements(by=By.CSS_SELECTOR, value=".job-card-container")

# Applying for the job
for listing in all_listings:
    print("I'm opening the listing for ...")
    print(listing)
    listing.click()
    time.sleep(2)
    try:
        apply_button = driver.find_element(By.CLASS_NAME, value="jobs-apply-button")
        apply_button.click()

        print("I'm applying...")
        next_step = driver.find_element(By.CLASS_NAME, value="artdeco-button--primary")
        n = 0

        more_steps = True
        while more_steps:
            try:
                next_step.click()
                n += 1
                print("I'm clickin buttons!")
                time.sleep(1)

                if n > 10:
                    print("Hm... Can't get through this one...")
                    abort_application()
                    more_steps = False
            except StaleElementReferenceException:
                print("Reviewing your application...")
                review_button = driver.find_element(By.CLASS_NAME, value="artdeco-button--primary")
                review_button.click()
                time.sleep(3)


    except NoSuchElementException:
        print("Must not be a button on here...")
