import requests
import json
import time
import plac
import os
import shutil

forum = "predictit"


@plac.annotations(thread_url=("Disqus thread URL", "positional", None, str),
                  apikey=("Disqus public API key", "positional", None, str),
                  dir_out=("Folder to store the output in", "positional", None, str),
                  limit=("Limit for cursor pagination", "option", None, int))
def main(thread_url: str, apikey: str, dir_out: str, limit: int = 100):
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

    # empty/create output directory:
    if os.path.isdir(dir_out):
        shutil.rmtree(dir_out)
    os.mkdir(dir_out)

    while True:
        response = requests.get(new_endpoint) # get API response
        if response.status_code != 200:
            print(f'Something went wrong. Response code: {response.status_code}')
            break
        out = response.json() # get json
        path_out = os.path.join(dir_out, f'posts_{doc_num}.json')
        json.dump(out, open(path_out, 'w')) # save to file
        print(f'Scraped page {doc_num}')
        doc_num += 1
        if out['cursor']['hasNext']:
            time.sleep(2) # some wait time
            new_endpoint = endpoint + f'&cursor={out["cursor"]["next"]}' # update endpoint with cursor
        else:
            print(f"No more pages left.")
            break


if __name__ == "__main__":
    plac.call(main)
