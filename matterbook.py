#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# coding=utf-8
import json
import logging
import os
import signal
import sys
import time

import facebook
import requests
import yaml

CONFIG_FILE = "matterbook.yml"

DATA_DIR = 'data'
LAST_POST_FILE_PATH = os.path.join(DATA_DIR, "last_post.txt")
FB_API_VERSION = '2.7'

log = logging.getLogger(__name__)


def main():
    setup_logging()
    log.info("Matterbook started")
    install_interrupt_handler()
    config = load_config()
    graph = get_graph_api(config)
    while True:
        check_post(graph, config)
        time.sleep(10)


def load_config():
    with open(CONFIG_FILE, 'r') as f:
        config = yaml.safe_load(f)
    log.debug("Config loaded")
    return config


def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        yaml.safe_dump(config, f, default_flow_style=False)
    log.debug("Config saved")
    return config


def check_post(graph, config):
    mm_config = config['mattermost']
    fb_config = config['facebook']
    page_id = fb_config['page_id']
    posts = graph.get_object(id=('%s/feed?fields=message,created_time,id&limit=1' % page_id))
    last_post = posts[u'data'][0]
    last_post_text = last_post['message'].encode("utf8")
    post_filter = fb_config.get('post_filter').encode("utf8")
    if post_filter == None or post_filter in last_post_text:
        if last_post == load_last_saved_post():
            log.debug("Old post: " + last_post_text)
        else:
            log.info("New post: " + last_post_text)
            username = mm_config.get('username')
            icon_url = mm_config.get('icon_url')
            basic_auth = mm_config.get('basic_auth')
            data = json.dumps({'username': username, 'text': last_post_text, 'icon_url': icon_url})
            webhook_url = mm_config['webhook_url']
            requests.post(webhook_url, data=data, auth=to_tuple(basic_auth))
            save_last_post(last_post)
    else:
        log.info("Ignoring: " + last_post_text)


def to_tuple(basic_auth):
    return tuple(basic_auth.values()) if basic_auth != None else None


def save_last_post(post):
    ensure_data_dir_exists()
    with open(LAST_POST_FILE_PATH, 'w') as f:
        json.dump(post, f)


def ensure_data_dir_exists():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def load_last_saved_post():
    ensure_data_dir_exists()
    if os.path.isfile(LAST_POST_FILE_PATH):
        with open(LAST_POST_FILE_PATH, 'r') as f:
            last_post = json.load(f)
    else:
        last_post = dict()
    return last_post


def get_graph_api(config):
    extended_token = get_extended_token(config)
    graph = facebook.GraphAPI(access_token=extended_token, version=FB_API_VERSION)
    return graph


def get_extended_token(config):
    fb_config = config['facebook']
    access_token = fb_config['access_token']
    app_id = fb_config['app_id']
    app_secret = fb_config['app_secret']
    graph = facebook.GraphAPI(access_token=access_token, version=FB_API_VERSION)
    extended_token_data = graph.extend_access_token(app_id, app_secret)
    extended_token = extended_token_data['access_token']
    fb_config['access_token'] = extended_token
    save_config(config)
    return extended_token


def install_interrupt_handler():
    signal.signal(signal.SIGINT, signal_handler)
    log.info('Press Ctrl+C or send SIGINT to exit')


def signal_handler(sig, frame):
    log.info('SIGINT received! Bye!')
    sys.exit(0)


def setup_logging():
    logging.basicConfig(format='%(asctime)s [%(module)s] %(message)s')
    log.setLevel(logging.INFO)


main()
