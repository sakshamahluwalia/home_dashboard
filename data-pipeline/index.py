from clients.alectra import main as alectra_main
from clients.brampton_water import main as brampton_water_main
from clients.enbridge import main as enbridge_main
from clients.reliance_water_heater import main as reliance_water_heater_main

from gen_helper.config import CONFIG
from gen_helper.driver import MyDriver
from gen_helper.db import connect_to_mongo, close_mongo_connection, write_bill_to_mongo

from msft_helper.auth import generate_token

from datetime import datetime

def main(driver, client):
    access_token = generate_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    service_provider_to_amount = {}
    service_provider_to_amount["Alectra"] = alectra_main(
        driver,
        username_of_user=CONFIG.alectra_username,
        password_of_user=CONFIG.alectra_password,
    )
    service_provider_to_amount["Brampton Water"] = brampton_water_main(
        driver,
        headers,
        username_of_user=CONFIG.brampton_water_username,
        password_of_user=CONFIG.brampton_water_password,
    )
    service_provider_to_amount["Enbridge"] = enbridge_main(headers)
    service_provider_to_amount["Reliance Water Heater"] = reliance_water_heater_main(headers)

    if client:
        current_month = datetime.now().month
        current_year = datetime.now().year
        for service_provider, amount in service_provider_to_amount.items():
            write_bill_to_mongo(client, service_provider, amount, current_month, current_year)
        


if __name__ == "__main__":
    my_driver = MyDriver()
    driver = my_driver.start_webdriver()
    client = connect_to_mongo()
    if client:
        main(driver, client)
    close_mongo_connection(client)
    my_driver.stop_webdriver()
