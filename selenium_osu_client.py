from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

CHROME_DRIVER_PATH = os.getenv("chrome_driver_path")
class OsuSeleniumClient:
    def __init__(self):
        self.chrome_service = webdriver.ChromeService(executable_path="./chromedriver-win64/chromedriver.exe")
        self.driver = webdriver.Chrome(service=self.chrome_service)
    
    def get_map_difficulties(self):
        
        all_difficulties_div = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "beatmapset-beatmap-picker"))
        )
        difficulties_tags = all_difficulties_div.find_elements(By.TAG_NAME, "a")
        all_beatmaps_ids = [link.get_attribute('href').split('/')[5] for link in difficulties_tags]
        all_beatmaps_names = []
        for difficulty in difficulties_tags:
            difficulty.click()
            difficulty_name = self.driver.execute_script("""return document.querySelector('.beatmapset-header__diff-name').innerText;""")
            if "mapped by" in difficulty_name:
                all_beatmaps_names.append(difficulty_name.split('mapped by')[0])
            else:
                all_beatmaps_names.append(difficulty_name.split("Star Rating")[0])
        data = {
            "beatmap_ids": all_beatmaps_ids,
            "beatmap_names": all_beatmaps_names
        }
        self.driver.quit()
        return data

        



    def osu_beatmapset_search(self):
        song_name = "first storm will stetson"
        url = f"https://www.google.com/search?q=osu {song_name}"
        self.driver.get(url=url)
        root = self.driver.find_element(By.CSS_SELECTOR, '.yuRUbf')
        span = root.find_element(By.TAG_NAME, "span")
        a_tag = span.find_element(By.TAG_NAME, "a")
        a_tag.click()
        self.get_map_difficulties()
        






seleniumClient = OsuSeleniumClient()

seleniumClient.osu_beatmapset_search()
    
