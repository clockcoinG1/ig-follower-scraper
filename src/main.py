import os
import time
import random
import uuid
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager as CM
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InstagramScraper:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.bot = self._initialize_bot()

    def _initialize_bot(self):
        options = webdriver.ChromeOptions()
        options.add_argument(
            f'--user-data-dir={os.environ["HOME"]}/Library/Application Support/Google/Chrome/Profile 1'
        )
        options.add_argument("--log-level=3")
        mobile_emulation = {
            "userAgent": (
                "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko)"
                " Chrome/90.0.1025.166 Mobile Safari/535.19"
            )
        }
        options.add_experimental_option("mobileEmulation", mobile_emulation)
        service = Service(executable_path=CM().install())
        return webdriver.Chrome(service=service, options=options)

    def login(self):
        self.bot.get('https://www.instagram.com/accounts/login/')
        time.sleep(1)
        try:
            element = self.bot.find_element(By.XPATH, "/html/body/div[4]/div/div/div[3]/div[2]/button")
            element.click()
        except NoSuchElementException:
            logging.info("** Instagram logged in already")
        time.sleep(5)

    def scrape_followers(self, usr, user_input):
        self.bot.get('https://www.instagram.com/{}/'.format(usr))
        time.sleep(3.5)
        WebDriverWait(self.bot, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/following')]"))
        ).click()
        time.sleep(2)
        logger.info('** Scraping...')
        users = set()
        for _ in range(round(user_input // 20)):
            ActionChains(self.bot).send_keys(Keys.END).perform()
            time.sleep(1)
        followers = self.bot.find_elements(By.XPATH, "//a[contains(@href, '/')]")

        for i in followers:
            if i.get_attribute('href'):
                users.add(i.get_attribute('href').split("/")[3])
            else:
                continue

        return users

    def save_followers(self, users, usr):
        logger.info(f'Saving {usr} followers...')
        with open(f'{usr}.followers.txt', 'a') as file:
            file.write('\n'.join(users) + "\n")
            logger.info(f'[DONE] - Your followers are saved in: {usr}.followers.txt file!')

    def close(self):
        logger.info('[bye!]')
        self.bot.quit()


def main():
    USERNAME = os.environ.get('USERNAME') if os.environ.get('USERNAME') else input('IG Username [leave blank if logged in]: ')
    PASSWORD = os.environ.get('PASSWORD') if os.environ.get('PASSWORD') else input('IG Password: [leave blank if logged in]: ')
    scraper = InstagramScraper(USERNAME, PASSWORD)
    scraper.login()

    usr = input('[Required] - Whose followers do you want to scrape: ')
    user_input = int(input('[Required] - How many followers do you want to scrape (60-500 recommended): '))

    followers = scraper.scrape_followers(usr, user_input)
    scraper.save_followers(followers, usr)
    scraper.close()


if __name__ == '__main__':
    main()
