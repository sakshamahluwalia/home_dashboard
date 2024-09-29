from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import requests

from gen_helper.config import CONFIG
from gen_helper.driver import MyDriver

"""
    Login to the Alectra website using the provided username and password
"""
def login_to_alectra(driver, username_of_user, password_of_user):
    # Open the Alectra website
    driver.get("https://myalectra.alectrautilities.com/portal/#/login")

    # Wait for the login form to load
    login_form = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "loginSection"))
    )

    # Find the username and password fields
    username = driver.find_element(By.ID, "username")
    password = driver.find_element(By.ID, "password")

    # Enter the username and password
    username.send_keys(username_of_user)
    password.send_keys(password_of_user)

    # Click the login button
    login_form_buttons = login_form.find_elements(By.TAG_NAME, "button")
    for button in login_form_buttons:
        if button.text.lower() == "log in":
            button.click()
            break


"""
    Get the access token from the cookies after logging in
"""
def get_access_token_from_cookies(driver):
    # After login, wait for a bit to ensure the cookies are set
    time.sleep(3)

    # Get all cookies from the driver
    cookies = driver.get_cookies()

    # Find and return the 'accessToken' cookie
    for cookie in cookies:
        if cookie["name"] == "accessToken":
            return cookie["value"]

    return None  # Return None if the cookie is not found


"""
    Get alectra billing data via API after getting the access token
"""
def get_billing_data_via_api_for_alectra(access_token):
    if access_token is None:
        print("Access token is None. Please login first.")
        return None
    # Make an API request to get the billing data
    url = f"https://alectra-svc.smartcmobile.link/apiservices/api/1/account/GetDashBoardBill?AccountNumber={CONFIG.alectra_account_number}"

    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        print("Request Successful!")
        return response.json()
    else:
        print(f"Request failed with status code {response.status_code}")
        print(response.text)
        return None


"""
    Extract the total charge using the API response
"""
def extract_total_charges_from_api_response(api_response):
    if api_response is None or "data" not in api_response or "projectedBill" not in api_response["data"]:
        return None
    # Extract the total charge from the API response
    data = api_response["data"]
    projected_bill = data["projectedBill"]
    return projected_bill


'''
    Main function to login to Alectra and extract the total charge
    @return: total_charge: float or None
'''
def main(driver, username_of_user, password_of_user):
    login_to_alectra(driver, username_of_user, password_of_user)
    WebDriverWait(driver, 5)
    access_token = get_access_token_from_cookies(driver)
    api_response = get_billing_data_via_api_for_alectra(access_token)
    total_charge = extract_total_charges_from_api_response(api_response)
    return float(total_charge) if total_charge else None



if __name__ == "__main__":
    my_driver = MyDriver()
    driver = my_driver.start_webdriver()
    total_charge = main(
        driver,
        username_of_user=CONFIG.alectra_username,
        password_of_user=CONFIG.alectra_password,
    )
    print(f"Total charge: {total_charge}")
    my_driver.stop_webdriver()