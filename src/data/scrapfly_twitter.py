import csv
import json
from typing import Any

import pandas as pd
from playwright.sync_api import sync_playwright
from scrapfly import ScrapflyClient, ScrapeConfig

SCRAPFLY = ScrapflyClient(key="scp-live-4efb5610f6474b7c9f9a461f5a70e4d5")

#result = SCRAPFLY.scrape(ScrapeConfig("https://twitter.com/Scrapfly_dev",  # we can enable features like:
#                                      # cloud headless browser use
#                                      render_js=True,  # anti scraping protection bypass
#                                      asp=True,  # screenshot taking
#                                      screenshots={"all": "fullpage"},  # proxy country selection
#                                      country="US", ))


def scrape_tweet_playwright(url: str) -> tuple[Any, Any]:
    """
    Scrape a single tweet page for Tweet thread e.g.:
    https://twitter.com/Scrapfly_dev/status/1667013143904567296
    Return parent tweet, reply tweets and recommended tweets
    """
    _xhr_calls = []

    def intercept_response(response):
        """capture all background requests and save them"""
        # we can extract details from background requests
        if response.request.resource_type == "xhr":
            _xhr_calls.append(response)
        return response

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False)
        context = browser.new_context(no_viewport=True)
        #context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()

        # enable background request intercepting:
        page.on("response", intercept_response)
        # go to url and wait for the page to load
        page.goto(url)
        try:
            page.wait_for_selector("[data-testid='tweet']", timeout=1500)
        except:
            return url.split("/")[-1], None

        # find all tweet background requests:
        tweet_calls = [f for f in _xhr_calls if "TweetResultByRestId" in f.url]
        for xhr in tweet_calls:
            data = xhr.json()
            data = data['data']['tweetResult']
            if 'result' in data and data['result']['__typename'] != 'TweetUnavailable':

                data = data['result']
                if 'tweet' in data:
                    data = data['tweet']
                return url.split("/")[-1], data['legacy']['full_text']
            else:
                return url.split("/")[-1], None


async def scrape_tweet_scrafly(url: str) -> tuple[Any, Any]:
    """
    Scrape a single tweet page for Tweet thread e.g.:
    https://twitter.com/Scrapfly_dev/status/1667013143904567296
    Return parent tweet, reply tweets and recommended tweets
    """
    result = await SCRAPFLY.async_scrape(ScrapeConfig(url, render_js=True,  # enable headless browser
                                                      wait_for_selector="[data-testid='tweet']"
                                                      # wait for page to finish loading
                                                      ))
    # capture background requests and extract ones that request Tweet data
    _xhr_calls = result.scrape_result["browser_data"]["xhr_call"]
    tweet_call = [f for f in _xhr_calls if "TweetResultByRestId" in f["url"]]
    for xhr in tweet_call:
        if not xhr["response"]:
            continue
        data = json.loads(xhr["response"]["body"])
        data = data['data']['tweetResult']
        if 'result' in data and data['result']['__typename'] != 'TweetUnavailable':
            data = data['result']
        else:
            return url.split("/")[-1], None
        return data['rest_id'], data['legacy']['full_text']
    # return url.split("/")[-1], None


if __name__ == "__main__":

    folder_path = '../../data/corpus_for_sexism_french/'

    df = pd.read_csv(f'{folder_path}corpus_with_link.csv')

    df_out = pd.DataFrame(columns=['index', 'tweet_id', 'tweet_text'])


    i = 8400

    for index, row in df.itertuples():
        if index < i:
            continue
        print(f"index : {index},\nrow : {row}")

        tweet_id, tweet_text = scrape_tweet_playwright(str(row))
        print(tweet_id, tweet_text)
        df_out.loc[len(df_out)] = [index, tweet_id, tweet_text]


        i += 1
        if i % 100 == 0:
            df_out.to_csv(f"{folder_path}corpus_with_text_df_{i}.csv", mode='a')
            df_out = pd.DataFrame(columns=['index', 'tweet_id', 'tweet_text'])
