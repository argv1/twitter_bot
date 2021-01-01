#!/usr/bin/env python3
'''
    Small script to follow twitter users
'''

from configparser import ConfigParser
from getpass import getpass
import logging
import os
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
import sys

# Time delay in seconds to wait for slow pages to load
page_delay = 1

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


class Twitter_Bot:
    def __init__(self):
        logger.info('Create Clas and open chrome')
        self.driver = None

    def open_browser(self):
        self.driver = webdriver.Chrome(executable_path=browser)
        self.driver.maximize_window()
 
    def login_to_twitter(self, username, password):
        logger.info('Navigating to twitter')
        try:
            self.driver.get('https://twitter.com/login')

            username_field = self.driver.find_element_by_name('session[username_or_email]')
            password_field = self.driver.find_element_by_name('session[password]')

            username_field.send_keys(username)
            self.driver.implicitly_wait(page_delay)
            
            password_field.send_keys(password)
            self.driver.implicitly_wait(page_delay)
            password_field.submit()
            logger.info('Login successful')
        
        except:
            print('Not able to login!')
            sys.exit(1)

    def subscribe(self, users):
        for user in users:
            try:
                self.driver.get(f'https://twitter.com/intent/user?screen_name={user}')
                self.driver.implicitly_wait(page_delay)
                self.driver.find_element_by_xpath('//div[@data-testid="confirmationSheetConfirm"]').click()
                logger.info(f'Successful subscribed to @{user}')
            except:   #mehrere exceptions, eine für bereits aboniert, eine für seite bzw user gibt es nicht
                logger.info(f'Subscribtion to @{user} not possible')     
                # wenn ich erneutes login auslösen will brauche ich die credentials, kann ich die vererben?          

    def run(self, username, password, users):
        self.open_browser() 
        self.login_to_twitter(username, password)
        self.subscribe(users)
        self.driver.quit()

def create_list(lines):
    entries = []
    for line in lines:
        users = line.split('@')
        users.pop(0)
        entries.extend(users)
    return entries

def main():
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

    # prepare file with user names
    with twitter_f.open('r') as f:
        lines = f.read().splitlines()
    users = create_list(lines)
    
    while True:
        # create Twitter Bot
        twitter = Twitter_Bot()
        try:
            # login and subscribe
            twitter.run(username, password, users)
        except:
            twitter.driver.quit()

if __name__  == '__main__':
    main()