# from active_checker import HOMEPAGE_URL, URL
import json
import os
import string
import random
import urllib
import re

from urllib.parse import urlparse, urlunparse, parse_qs
import yaml

from playwright.sync_api import Request

import utils
from utils import fuzz_open

from config import config

## TYPE-ALIAS
URL = str ## For example, http://localhost/wordpress/admin.php

def load_config(config_path='config.yaml'):
    with open(config_path, encoding="utf-8_sig") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

    print('Config loaded.')  # Just to show that it only loads once.
    return data

def is_token_key(key):
    # Heuristics: keys that are long random hex or base32/64-like
    try:
        return bool(re.fullmatch(r'[a-fA-F0-9]{8,}', key)) or bool(re.fullmatch(r'[a-zA-Z0-9]{10,}', key))
    except Exception as e:
        print(f"[GENERALFUNCTION] Failed in is_token_key: {e}")
    return False

def is_token_value(value):
    # Heuristics: values that are long and look like hashes or non-dictionary words
    try:
        return bool(re.fullmatch(r'[a-fA-F0-9]{10,}', value)) or bool(re.fullmatch(r'[a-zA-Z0-9+/=]{20,}', value))
    except Exception as e:
        print(f"[GENERALFUNCTION] Failed in is_token_value: {e}")
    return False

def identify_security_params(url):
    parsed_url = urlparse(url)
    normalized_query = parsed_url.query.replace(';', '&')
    params = parse_qs(normalized_query)

    tokens = {}
    for key, values in params.items():
        key_flag = is_token_key(key)
        value_flag = any(is_token_value(v) for v in values)
        if key_flag or value_flag:
            tokens[key] = values
            # print(f"[FUNCTION] Getting token value: {values}")
    return tokens

def filterbyvalue(seq, value):
    for el in seq:
        if el.attribute==value:
            yield el

def clean_base_url(base_url):
    """Keeps only the scheme and netloc (domain) of the base URL."""
    parsed = urlparse(base_url)
    cleaned = parsed._replace(path='', params='', query='', fragment='')
    return urlunparse(cleaned)

def is_same_domain(url: URL):
    base_url = clean_base_url(config.data["HOMEPAGE_URL"])

    if (url.find(base_url)>-1):
        return True

    if (url.find("http://")>-1 or url.find("https://")>-1):
        return False
    else:
        return True

def get_full_link(url):
    """
    to ensure that the given url is written in complete url. Some crawled links may only put incomplete url like 'new.php'
    :param url:
    :return:
    """
    if (url.find(config.data["HOMEPAGE_URL"])==0):
        return url

    if (url.find("http://")==0 or url.find("https://")==0):
        return url
    else:
        if url.find("/")==0:
            parsed_url = urlparse(config.data["HOMEPAGE_URL"])
            return f"{parsed_url.scheme}://{parsed_url.netloc}{url}"
        else:
            if config.data["HOMEPAGE_URL"][-1:]=="/":
                return config.data["HOMEPAGE_URL"]+url
            else:
                return config.data["HOMEPAGE_URL"]+"/"+url

def get_absolute_link(url, current_page_url):
    return str(urllib.parse.urljoin(current_page_url,url))

def get_complete_link(url, current_page_url):
    """
    to ensure that the given url is written in complete url. Some crawled links may only put incomplete url like 'new.php'
    :param url:
    :return:
    """
    if (url.find(config.data["HOMEPAGE_URL"])==0):
        return url

    if (url.find("http://")==0 or url.find("https://")==0):
        return url
    else:
        if url.find("/")==0:
            parsed_url = urlparse(config.data["HOMEPAGE_URL"])
            return f"{parsed_url.scheme}://{parsed_url.netloc}{url}"
        else:
            if config.data["HOMEPAGE_URL"][-1:]=="/":
                return current_page_url+url
            else:
                return current_page_url+"/"+url

def print_request(request: Request):
    if request.method=="POST":
        print(">> a Post Request is detected", request, request.headers, request.post_data_json)

def randomword(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def save_credentials(playwright, user, path):
    """
    Save user credential in a JSON file for being used by other functions
    :param playwright:
    :return:
    """
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto(config.data["HOMEPAGE_URL"])
    page.get_by_label("Username or Email Address").fill(user['username'])
    page.get_by_label("Password", exact=True).fill(user['password'])
    page.get_by_role("button", name="Log In").click()
    page.wait_for_load_state()

    page.context.storage_state(path=path)

    context.close()
    browser.close()

def manually_save_credentials(playwright, path):
    """
    Save user credential in a JSON file for being used by other functions
    :param playwright:
    :return:
    """
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto(config.data["HOMEPAGE_URL"])
    page.wait_for_load_state()

    page.pause()

    page.context.storage_state(path=path)

    context.close()
    browser.close()

def read_cov_from_file(coverage_file_path):
    if not os.path.exists(coverage_file_path):
        print("[GENERALFUNCTION] Path does not exist: ",coverage_file_path)
        return 0,0

    with fuzz_open(coverage_file_path, "r", isCompress=True) as f:
        try:
            coverage_report = json.load(f)
        except Exception as e:
            coverage_report = None
            print(f"[GENERALFUNCTION] {e}")

    if not coverage_report:
        print("[GENERALFUNCTION] Error in Loading the cov file")
        return 0,0

    hit_paths = utils.extract_hit_paths(coverage_report)
    stringified_hit_paths = set(utils.stringify_hit_paths(hit_paths))
    utils.all_lines_count_dict(hit_paths, config.line_coverage)
    hit_path_set = set(stringified_hit_paths)
    print(f"[GENERALFUNCTION] Found {len(hit_path_set)} of hit_path_set")

    return hit_path_set, stringified_hit_paths


import re

def extract_sql_command_and_table(query):
    # Normalize query to ignore case and remove extra whitespace
    normalized = ' '.join(query.strip().split()).lower()

    patterns = {
        'insert': r'insert\s+into\s+`?(\w+)`?',
        'update': r'update\s+`?(\w+)`?',
        'delete': r'delete\s+from\s+`?(\w+)`?'
    }

    for command, pattern in patterns.items():
        match = re.search(pattern, normalized, re.IGNORECASE)
        if match:
            return command.upper(), match.group(1)

    return None, None
