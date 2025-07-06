from enum import Enum
import selenium.webdriver
import selenium.webdriver.edge.service
import selenium.webdriver.chrome.service
from selenium.webdriver.support.wait import WebDriverWait


class Config:
    class Browser(Enum):
        Chrome = 0,
        Edge = 1

    BROWSER: Browser = Browser.Edge
    DRIVER_PATH: str = R'.driver\msedgedriver.exe'
    WAIT_TIME: float = 3

    @staticmethod
    def get_resolver() -> tuple:
        if Config.BROWSER == Config.Browser.Chrome:
            chrome_options = selenium.webdriver.ChromeOptions()
            chrome_service = selenium.webdriver.chrome.service.Service(Config.DRIVER_PATH)
            chrome_driver = selenium.webdriver.Chrome(service=chrome_service, options=chrome_options)
            return chrome_driver, WebDriverWait(chrome_driver, Config.WAIT_TIME)

        elif Config.BROWSER == Config.Browser.Edge:
            edge_options = selenium.webdriver.EdgeOptions()
            # edge_options.add_argument('--headless')
            edge_options.add_argument('--start-maximized')
            edge_options.add_argument('--disable-blink-features=AutomationControlled')
            edge_options.add_experimental_option('excludeSwitches', ['enable-automation'])

            edge_service = selenium.webdriver.edge.service.Service(Config.DRIVER_PATH)
            edge_driver = selenium.webdriver.Edge(service=edge_service, options=edge_options)
            return edge_driver, WebDriverWait(edge_driver, Config.WAIT_TIME)

        return None, None
