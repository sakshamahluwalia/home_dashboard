from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


class MyDriver:

    def __init__(self):
        self.driver = None
        self.service = Service(
            executable_path="/Users/sakshamahluwalia/Downloads/chromedriver-mac-arm64/chromedriver"
        )

    def start_webdriver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])

        # Specify the path to the Chromium binary
        chrome_options.binary_location = '/usr/bin/chromium'

        # Specify the path to Chromedriver
        service = Service('/usr/bin/chromedriver') 

        # self.driver = webdriver.Chrome(service=self.service)
        
        # Initialize the driver with the specified service and options
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

        return self.driver

    def stop_webdriver(self):
        # Close the webdriver
        self.driver.close()
