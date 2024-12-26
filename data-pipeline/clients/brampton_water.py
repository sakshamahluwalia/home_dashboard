from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from gen_helper.driver import MyDriver
from gen_helper.config import CONFIG
from msft_helper.auth import generate_token
from msft_helper.outlook_client import fetch_brampton_water_email_from_junk

import time
import re
from datetime import datetime

"""
    Login to the Alectra website using the provided username and password
"""
def login(driver, username_of_user, password_of_user):
    # Open the Alectra website
    driver.get("https://peelregion.idoxs.ca/authentication/login")

    # Wait for the page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "bannerSignInUsername"))
    )

    # Find the username and password fields
    username = driver.find_element(By.ID, "bannerSignInUsername")
    password = driver.find_element(By.ID, "bannerSignInPassword")

    # Enter the username and password
    username.send_keys(username_of_user)
    password.send_keys(password_of_user)

    login_button = driver.find_element(By.ID, "btnSignIn")
    login_button.click()


"""
    This function uses a regular expression to extract the OTP from the email subject.
"""
def _extract_otp_from_subject(subject):
    # Adjust the pattern based on your OTP format. Here, we assume it's a 6-digit number.
    otp_pattern = r"\b\d{6}\b"
    match = re.search(otp_pattern, subject)
    if match:
        return match.group(0)  # Return the OTP if found
    return None


"""
    Fetch the OTP from outlook email subject
"""
def fetch_otp_from_email(msft_auth_headers):

    emails = fetch_brampton_water_email_from_junk(
        msft_auth_headers,
        CONFIG.brampton_water_subject_filter,
        CONFIG.brampton_water_sender_filter,
    )

    otp = None
    # download attachments
    if not emails:
        print("No emails found matching the criteria.")
    else:
        for email in emails:
            subject = email.get("subject", "")
            otp = _extract_otp_from_subject(subject)
            if otp:
                print(f"Found OTP: {otp} in subject: {subject}")
            else:
                print(f"No OTP found in subject: {subject}")
    return otp


"""
    Finish the login process using the OTP
"""
def finish_login_using_otp(driver, otp):
    # Find the OTP field
    otp_field = driver.find_element(By.ID, "main_VerifyCtrl_txtCode")
    otp_field.send_keys(otp)

    # Click the "Sign In" button
    sign_in_button = driver.find_element(By.ID, "main_VerifyCtrl_btnVerifyCode")
    sign_in_button.click()


def navigate_to_bill_page(driver):
    # Click the "View Bill" button
    time.sleep(5)
    billing_and_payment_button = driver.find_element(By.ID, "billing-and-payment")
    billing_and_payment_button.click()

    # Click the "View Bill" card
    time.sleep(5)
    view_bill_card = driver.find_elements(By.CLASS_NAME, 'section-title')[0]
    view_bill_card.click()


"""
    Extract the total charge from the webpage
"""
def extract_total_charges_from_webpage(driver):
    # Wait for the page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "main_ctl09_lblAmountDue"))
    )
    # Find the total charge element
    total_charge_element = driver.find_element(By.ID, "main_ctl09_lblAmountDue")
    total_charge = total_charge_element.text.replace("$", "")

    due_date_element = driver.find_element(By.ID, "main_ctl09_lblDueDate")
    due_date = due_date_element.text

    date_obj = datetime.strptime(due_date, '%B %d, %Y')
    return total_charge, date_obj.month, date_obj.year



'''
    Main function to login to Brampton water and extract the total charge
    @return: total_charge: float or None
'''
def main(driver, msft_auth_headers, username_of_user, password_of_user):
    try:
        login(driver, username_of_user, password_of_user)
        time.sleep(10)
        otp = fetch_otp_from_email(msft_auth_headers)
        if otp:
            finish_login_using_otp(driver, otp)

            navigate_to_bill_page(driver)
            total_charge, month, year = extract_total_charges_from_webpage(driver)
            return {"total_charge": total_charge if total_charge else 0, "month": month, "year": year}
        else:
            print("Could not login to Brampton water.")
            return None
    except Exception as e:
        print(f"failed to get bill for bramtpon water {str(e)}")


if __name__ == "__main__":
    # get emails
    access_token = generate_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    # Start / Setup the webdriver
    my_driver = MyDriver()
    driver = my_driver.start_webdriver()
    total_charge = main(
        driver,
        headers,
        username_of_user=CONFIG.brampton_water_username,
        password_of_user=CONFIG.brampton_water_password,
    )
    print(f"Total charge for brampton water: {total_charge}")
    my_driver.stop_webdriver()
