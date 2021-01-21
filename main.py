#!/usr/bin/env python3
'''
    Twitter bot to automate stuff using selenium
    
'''

from configparser import ConfigParser
from getpass import getpass
import logging
import os
from pathlib import Path
import twitterbot

# Time delay in seconds to wait for slow pages to load
page_delay = 2

# Define path and filename
base_path = Path(__file__).parent.absolute()
twitter_f = base_path / 'twitter_users.txt'  
log_f = base_path / 'run.log'
config_f = base_path / 'config.ini'
browser = base_path / 'chromedriver.exe'

# Setup Logging
logger = logging.getLogger('twitter_logger')
logger.setLevel(logging.DEBUG)

# create log file handler
fh = logging.FileHandler(log_f)
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)

# create stream handler (console output)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

# set format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)

logger.info(f'Logger initialized. Log file {log_f} is being saved to {os.getcwd()}')

def create_list(lines):
    entries = []
    for line in lines:
        users = line.split('@')
        users.pop(0)
        [entries.append(user.replace(' ','')) for user in users]     
    return entries

def credentials():
    # get credentials
    config_file = ConfigParser()
    config_file.read(config_f)
    settings = config_file['SETTINGS']
    try:
        username = settings['Username']
    except KeyError:
        username = input('[?] Twitter Username: ')
    try:
        password = settings['Password']
    except KeyError:
        password = getpass(f'[?] Twitter Password for {username}: ')
    return username, password

def main():
    username, password = credentials()

    # prepare file with user names
    with twitter_f.open('r') as f:
        lines = f.read().splitlines()
    users = create_list(lines)
    
    # create Twitter Bot
    twitter = twitterbot.Bot(username, password, browser, logger, page_delay)

    try:
        # login and subscribe
        twitter.subscribe(users)
    except:
        logger.info('An error occured.')
    finally:
        twitter.driver.quit()

if __name__  == '__main__':
    main()
