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

from bs4 import BeautifulSoup
from pathlib import Path
import os
import re
import requests

SCRIPT_DIR    = os.path.dirname(os.path.realpath(__file__)) + "/rss-ntfy/"
SERVICES      = [
                 {
                  "service": "nitter", 
                  "rss-url": "https://uk.unofficialbird.com/{{ custom }}/rss", 
                  "descriptor": "🐦 Tweet"
                 },
                 {
                  "service": "proxitok", 
                  "rss-url": "https://proxitok.pabloferreiro.es/@{{ custom }}/rss", 
                  "descriptor": "🎶 TikTok"
                 },
                 {
                  "service": "invidious", 
                  "rss-url": "https://invidious.snopyta.org/feed/channel/{{ custom }}",
                  "descriptor": "📽 YouTube video"

                 },
                 { 
                  "service": "teddit",
                  "rss-url": "https://teddit.net/r/{{ custom }}?api&type=rss",
                  "descriptor": "🎩 Reddit post" 
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

def handlebar_replace(input, replacement):
    '''
    Very simple Handlebar style replace:
    https://handlebarsjs.com

    Takes the input URL and replaces the {{ custom }}
    part, which will be the current user part.
    '''
    return re.sub('\{\{.*\}\}', replacement, input)

def check_file_list_exists(file_list):
    '''
    Takes a list of files, checks if they exist, 
    creates them if they do not!

    I'm using this function instead of just relying on
    'w+', because we 'r+' the History file, at one point,
    and 'r+' doesn't create the file if it doesn't exist 
    (unlike 'w+' and 'a+').
    '''
    for file in file_list:
        Path(file).touch(exist_ok=True)

def main():
    '''
    This article by Matthew Wimberly got me along the right lines with things:
    https://codeburst.io/building-an-rss-feed-scraper-with-python-73715ca06e1f
    '''
    for service in SERVICES:
        # Follow File and History File
        user_list_file = f"{SCRIPT_DIR}{service['service']}-follow-list.txt"
        service_hist   = f"{SCRIPT_DIR}{service['service']}_hist"
        check_file_list_exists([user_list_file, service_hist])

        # Instance, Topic, Descriptor
        instance    = f"{service['rss-url']}"
        ntfy_topic  = f"{service['service']}"
        descriptor  = service['descriptor']

        # TODO: Rename everything with 'user', as it's more generally an
        #       account? Not sure if account is the best name, either.
        user_list   = get_user_list(user_list_file)

        for username in user_list:
            current_instance = handlebar_replace(instance, username)
            try:
                req = requests.get(f"{current_instance}")
                rss_content = BeautifulSoup(req.content, "lxml-xml")
                articles = rss_content.findAll('item')
                for a in articles:
                    title     = a.find('title').text
                    link      = a.find('link').text
                    published = a.find('pubDate').text

                    with open(service_hist, "r+") as hist_file:
                        data = hist_file.read()
                        # If the link isn't in data, not only
                        # do we want to add it to the Hist file,
                        # we also want to, of course, ntfy:
                        if not link in data:
                            ntfyr_complex(ntfy_topic, 
                                          username, 
                                          title, 
                                          link, 
                                          published,
                                          descriptor)
                            hist_file.write(f"{link}\n")

            except Exception as e:
                # TODO: Just use the ntfy JSON request format
                ntfyr(f"Error with scraping {username}, '{e}'.", ntfy_topic)

if __name__ == '__main__':
    main()
