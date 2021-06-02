import requests
import json
import time
import plac
import os
from util import retry

forum = "predictit"


@retry(tries=5, delay=5, backoff=5)
def scrape_endpoint(endpoint: str):
    response = requests.get(endpoint)
    if response.status_code != 200:
        raise ConnectionRefusedError(f"Status code: {str(response.status_code)}")
    out = response.json()  # get json
    return out


@plac.annotations(thread_url=("Disqus thread URL", "positional", None, str),
                  apikey=("Disqus public API key", "positional", None, str),
                  dir_out=("Folder to store the output in", "positional", None, str),
                  limit=("Limit for cursor pagination", "option", None, int),
                  sleep_time=("Sleep time between API requests", "option", None, int))
def main(thread_url: str, apikey: str, dir_out: str, limit: int = 100, sleep_time: int = 1):
    """
    Extract Disqus comments from Predictit using Disqus API listPosts method with cursor.

    :param thread_url: Thread URL for the specific Disqus thread on Predicit website.
            Can be extracted using get_thread_id.pu
    :param apikey: Disqus public API Key
    :param dir_out: output directory
    :param limit: cursor limit for the API (100 is max)
    :return:
    """
    doc_num = 0
    # set up base endpoint (first result)
    endpoint = "https://disqus.com/api/3.0/threads/listPosts.json?"
    endpoint += f"api_key={apikey}&forum={forum}&thread:link={thread_url}&limit={limit}"
    new_endpoint = endpoint

    while True:
        out = scrape_endpoint(new_endpoint)  # get json
        path_out = os.path.join(dir_out, f'posts_{doc_num}.json')
        json.dump(out, open(path_out, 'w'))  # save to file
        print(f'Scraped page {doc_num}')
        doc_num += 1
        if out['cursor']['hasNext']:
            time.sleep(sleep_time)  # some wait time
            new_endpoint = endpoint + f'&cursor={out["cursor"]["next"]}'  # update endpoint with cursor
        else:
            print(f"No more pages left.")
            break


if __name__ == "__main__":
    plac.call(main)
