#get url here 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import chromedriver_autoinstaller
import time

def geturl(pkcard):
    card_name = pkcard
    chromedriver_autoinstaller.install()
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    chromedriver_path = "/home/appuser/.cache/selenium/chromedriver/linux64/133.0.6943.98/chromedriver"
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get("https://www.pricecharting.com/")
        textbox = driver.find_element(By.ID, 'game_search_box')
        textbox.send_keys(card_name)
        textbox.send_keys(Keys.RETURN)
        element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "game-page")))
        print(f"Element: {element}, \nLength of element {not element}")
        #Check if search results exist
        if  not element:
            driver.find_elements(By.ID, "search-results") #WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID, "game-page"))) == "not null":
            driver.find_elements(By.ID, "search-results")
            table = driver.find_element(By.ID, "games_table")
            tbody = table.find_element(By.TAG_NAME, "tbody")
            
            #Locate the first row and click the title link
            first_row = tbody.find_element(By.TAG_NAME, "tr")
            title_link = first_row.find_element(By.CLASS_NAME, 'title').find_element(By.TAG_NAME, 'a')

            #Click the link and wait for the new page
            title_link.click()
            url = driver.current_url
            print(f"Game page URL: {url}")
            return url
        else:
            driver.find_elements(By.ID, "game-page")
            url = driver.current_url
            print(f"Already on the game page: {url}")
            return url
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

