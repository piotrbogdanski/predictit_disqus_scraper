from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import plac
import re


@plac.annotations(
    url=("Predictit URL to find Disqus thread url", "positional", None, str)
)
def main(url):
    """
    Open Predictit URL using Selenium to find the Disqus thread URL. Write the thread url to url.txt.
    :param url: Predictit URL to find Disqus thread url
    :return: None
    """
    # Set up Selenium webdriver in headless mode:
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)

    # open Predictit url
    driver.get(url)

    # xpath to find the Disqus iframe. Adopted from:
    # https://github.com/louisguitton/disqus-crawler/blob/master/disqus-crawler/spiders/url_grabber.py
    xpath = "//iframe[contains(@src,'http://disqus.com') or contains(@src,'https://disqus.com')]"
    try:
        elem = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, xpath))) # obtain element
        src = elem.get_attribute("src") # get the Disqus src
        # extract thread_url:
        thread_url = [match.group(0) for u in src.split('&') if (match := re.search(r"(?<=t_u\=).+", u))][0]
        print(f"Extracted thread link: {thread_url}")
        # write output:
        with open('url.txt', 'w') as f:
            f.write(thread_url)
    except Exception as e:
        print(f"Exception: {e}")
    driver.quit()


if __name__ == "__main__":
    plac.call(main)
