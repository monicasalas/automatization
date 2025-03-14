from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

class CustomWebDriver:
    def __init__(self, driver_path="C:\Program Files (x86)\chromedriver-win64\chromedriver.exe"):
        self.driver_path = driver_path
        self.options = Options()

        self.options.add_argument("--disable-blink-features=AutomationContolled")
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option("useAutomationExtension", False)

        #User-Agent
        self.options.add_argument(
                                  "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
                                  )
        
    def get_driver(self):
        #Regresa una instancia del WebDriver
        service = Service(self.driver_path)
        driver = webdriver.Chrome(service=service, options=self.options)

        #Desabilita ´navigator.webdriver´
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        return driver