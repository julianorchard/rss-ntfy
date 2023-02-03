#!/usr/bin/env python3

##   rss-ntfy.py  ---  Scrape RSS feeds and ntfy yourself.

# Copyright (c) 2023   Julian Orchard <jorchard@pm.me>

## Description:

# Really simple RSS feed scraper that looks at a list of URL's
# and sends a little ntfy about it.

# Mainly designed for Proxitok and Nitter.

## License:

# See /LICENSE file in the root of this repository.

## Code:

import os
import requests
from bs4 import BeautifulSoup

SCRIPT_DIR    = os.path.dirname(os.path.realpath(__file__)) + "/rss-ntfy/"
SERVICES      = [
                 {
                  "service": "nitter", 
                  "rss-url": "https://uk.unofficialbird.com/{username}/rss", 
                  "descriptor": "🎶 Tweet"
                 },
                 {
                  "service": "proxitok", 
                  "rss-url": "https://proxitok.pabloferreiro.es/@{username}/rss", 
                  "descriptor": "🎶 TikTok"
                 },
                 {
                  "service": "invidious", 
                  "rss-url": "https://invidious.snopyta.org/feed/channel/{username}", 
                  "descriptor": "📽 YouTube video "
                 }
                ]
NTFY_INSTANCE = "https://ntfy.julian.rocks/"


def ntfyr(message, ntfy_topic):
    '''
    This just uses the simple example on docs.ntfy.sh to
    send a message via ntfy.
    '''
    requests.post(f'{NTFY_INSTANCE}{ntfy_topic}', data=f"{message}".encode(encoding="UTF-8"))

def ntfyr_complex(ntfy_topic, username, title, link, published, description):
    '''
    This sends a more complicated notification via ntfy.

    It's more based around the example of 'using a JSON
    array', below:
    https://docs.ntfy.sh/publish/
    '''
    message_text = f"{description} from {username}"
    if title != "":
        message_text = f"{message_text}:\n\n{title}!"
    else:
        message_text = f"{message_text}!"
    requests.post(f"{NTFY_INSTANCE}",
        json = {
            "topic": f"{ntfy_topic}",
            "message": f"{message_text}",
            "actions": [{
                "action": "view",
                "label": "View!",
                "url": f"{link}"
            }]
        }
    )

def get_user_list(user_list_file):
    '''
    Get the users list into a list to iterate.
    '''
    with open(user_list_file, encoding="UTF-8") as f:
        user_list = [l.rstrip() for l in f]
    return user_list

def main():
    '''
    This article by Matthew Wimberly got me along the right lines with things:
    https://codeburst.io/building-an-rss-feed-scraper-with-python-73715ca06e1f
    '''
    for service in SERVICES:
        user_list_file = f"{SCRIPT_DIR}{service['service']}-follow-list.txt"
        instance       = f"{service['rss-url']}"
        ntfy_topic     = f"{service['service']}"
        service_log    = f"{SCRIPT_DIR}{service['service']}.log"
        descriptor     = service['descriptor']
        user_list = get_user_list(user_list_file)
        for username in user_list:
            try:
                req = requests.get(f"{instance}")
                rss_content = BeautifulSoup(req.content, "lxml-xml")
                articles = rss_content.findAll('item')
                for a in articles:
                    title     = a.find('title').text
                    link      = a.find('link').text
                    published = a.find('pubDate').text

                    with open(service_log, "r+") as f:
                        data = f.read()
                        if not link in data:
                            ntfyr_complex(ntfy_topic, 
                                          username, 
                                          title, 
                                          link, 
                                          published,
                                          descriptor)
                            f.write(f"{link}\n")

            except Exception as e:
                ntfyr(f"Error with scraping {username}, '{e}'.", ntfy_topic)

if __name__ == '__main__':
    main()
