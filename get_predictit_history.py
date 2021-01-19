from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import shutil
import os
from util import retry
import glob
import plac


@retry()
def wait_and_click(driver, cond, wait_time: int = 10):
    WebDriverWait(driver, wait_time).until(cond).click()


@retry()
def move_csv(directory, path_move):
    filename = max(glob.glob(directory + '/*.csv'), key=os.path.getctime)
    shutil.move(filename, path_move)
    print(f'Saved file {filename} to {path_move}')


@plac.annotations(url=("Url to extract data from", "positional", None, str),
                  out_dir=("Dir to store the output", "positional", None, str))
def main(url: str, out_dir: str):
    # setup
    directory = os.path.abspath(out_dir)
    profile = webdriver.FirefoxProfile()
    profile.set_preference('browser.download.folderList', 2)  # custom location
    profile.set_preference('browser.download.manager.showWhenStarting', False)
    profile.set_preference('browser.download.dir', directory)
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')
    options = webdriver.FirefoxOptions()
    options.headless = True

    # initialize driver
    driver = webdriver.Firefox(firefox_profile=profile, options=options)

    # get url:
    driver.get(url)

    cond = EC.element_to_be_clickable((By.LINK_TEXT, "90 Day"))
    wait_and_click(driver, cond, 10)

    cond = EC.element_to_be_clickable((By.CLASS_NAME, "charts-header__download"))
    wait_and_click(driver, cond, 10)

    move_csv(directory, os.path.join(directory, 'markets.csv'))
    driver.close()


if __name__ == "__main__":
    plac.call(main)
