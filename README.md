# Scraping Disqus comments from Predictit

This repo contains collection of Python scripts (using Selenium and Disqus API) 
which allow you to extract comments and historical data from a Predictit prediction market specify by its URL
(for example: https://www.predictit.org/markets/detail/6994/Will-Donald-Trump-file-to-run-for-president-before-the-end-of-2021)

## Setup

- Clone the repo, create a virual environment and install the requirements:

```bash
git clone git@github.com:piotrbogdanski/predictit_disqus_scraper.git
cd predictit_disqus_scraper
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

- Install `geckodriver` and add it to your path following the instructions 
  [here](https://askubuntu.com/questions/870530/how-to-install-geckodriver-in-ubuntu) 
  (the project runs on  `v0.24.0-linux64.tar.gz`
  
- Place your [Disqus API public key](https://disqus.com/api/docs/) in file `disqus_key.txt` in the main project directory

- Specify market url and output directory in first two lines of `scrape.sh`

- Run `scrape.sh`.
