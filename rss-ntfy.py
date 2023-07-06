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
import yaml

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__)) + "/rss-ntfy/"
with open("config.yaml", "r") as config_file_contents:
    CONFIG = yaml.safe_load(config_file_contents)
NTFY_INSTANCE = "https://ntfy.sh/"


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
    return re.sub('{{.*}}', replacement, input)

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
    for service_name in CONFIG:
        # Follow File and History File
        user_list_file = f"{SCRIPT_DIR}{CONFIG[service_name]['service']}-follow-list.txt"
        service_hist   = f"{SCRIPT_DIR}{CONFIG[service_name]['service']}_hist"
        check_file_list_exists([user_list_file, service_hist])

        # Instance, Topic, Descriptor
        instance    = f"{CONFIG[service_name]['rss-url']}"
        ntfy_topic  = f"{CONFIG[service_name]['service']}-jdo-personal"
        descriptor  = CONFIG[service_name]['descriptor']

        # Alternative Tags Input
        item_tag    = CONFIG[service_name].get("item-alt",    "item")
        title_tag   = CONFIG[service_name].get("title-alt",   "title")
        link_tag    = CONFIG[service_name].get("link-alt",    "link")
        date_tag    = CONFIG[service_name].get("pubdate-alt", "pubDate")

        # TODO: Rename everything with 'user', as it's more generally an
        #       account? Not sure if account is the best name, either.
        user_list   = get_user_list(user_list_file)

        for username in user_list:
            current_instance = handlebar_replace(instance, username)
            name_tag = CONFIG[service_name].get("name-alt", username)
            try:
                req = requests.get(f"{current_instance}")
                rss_content = BeautifulSoup(req.content, "lxml-xml")
                articles = rss_content.findAll(item_tag)
                for a in articles:
                    title     = a.find(title_tag).text
                    link      = a.find(link_tag).text
                    published = a.find(date_tag).text

                    # If we need a different name from the username,
                    # handle that here.
                    if name_tag != username:
                        name = a.find(name_tag).text
                    else:
                        name = username

                    with open(service_hist, "r+") as hist_file:
                        data = hist_file.read()
                        # If the link isn't in data, not only
                        # do we want to add it to the Hist file,
                        # we also want to, of course, ntfy:
                        if not link in data:
                            ntfyr_complex(ntfy_topic,
                                          name,
                                          title,
                                          link,
                                          published,
                                          descriptor)
                            hist_file.write(f"{link}\n")

            except Exception as e:
                # TODO: Just use the ntfy JSON request format
                ntfyr(f"Error with scraping {name_tag}, '{e}'.", ntfy_topic)

if __name__ == '__main__':
    main()
