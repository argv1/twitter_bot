#!/usr/bin/env python3
'''
    Twitter bot to automate stuff using selenium
    
'''

from configparser import ConfigParser
from getpass import getpass
import logging
import os
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys 
import sys
import time

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

class TwitterBot:
    def __init__(self, username, password, ):
        self.driver = webdriver.Chrome(executable_path=browser)
        self.driver.maximize_window()
        self.username = username
        self.__password = password
        self.subscriptions = 0
        logger.info('Twitter bot class created and opened chrome')
 
    def __login_to_twitter(self):
        logger.info('Navigating to twitter')
        try:
            self.driver.get('https://twitter.com/login')
            time.sleep(page_delay)

            username_field = self.driver.find_element_by_name('session[username_or_email]')
            username_field.clear()
            username_field.send_keys(self.username)
            
            password_field = self.driver.find_element_by_name('session[password]')
            password_field.clear()
            password_field.send_keys(self.__password)
            password_field.submit()
            logger.info('Login successful')
        
        except:
            print('Not able to login!')
            sys.exit(1)

        try:
            # Accept cookies
            self.driver.find_element(By.CSS_SELECTOR, '.css-18t94o4:nth-child(2) > .css-901oao > .css-901oao > .css-901oao').click()
            logger.info('Cookies accepted.')
        except: 
            logger.info('No cookie notification.')

    def subscribe(self, users):
        self.__login_to_twitter()

        for user in users:
            try:
                self.driver.get(f'https://twitter.com/{user}')
                time.sleep(page_delay)

                # check if session is still logged in or need to relogin
                elem = self.driver.find_elements(By.CSS_SELECTOR, '.r-117bsoe > .css-901oao')
                if(len(elem) > 0 and (elem[0].text == 'Etwas ist schiefgelaufen.')):
                    logger.info(f'Relogin required')
                    users.append(user)
                    self.__login_to_twitter()
                    continue

                # check if user exist, if not pass
                elem = self.driver.find_elements(By.CSS_SELECTOR, '.r-yfoy6g > .r-jwli3a')
                if(len(elem) > 0 and (elem[0].text == 'This account doesn’t exist' or elem[0].text == 'Dieser Account existiert nicht')):
                    logger.info(f'User {user}does not exist.')
                    continue

                # follow user            
                self.driver.find_element(By.CSS_SELECTOR, '.css-1dbjc4n:nth-child(1) > .css-18t94o4:nth-child(1) > .css-901oao > .css-901oao > .css-901oao').click()
                logger.info(f'Successful subscribed to @{user}.')
                self.subscriptions += 1
            except:   
                logger.info(f'Subscribtion to @{user} not possible.') 

        logger.info(f'Successfully subscribed to {self.subscriptions} out of {len(users)}.') 
        self.logout()

    def logout(self):
        try:
            self.driver.get("https://twitter.com/home")
            time.sleep(page_delay)
            self.driver.find_element(By.CSS_SELECTOR, ".r-obd0qt > .r-jwli3a").click()
            time.sleep(page_delay)
            self.driver.find_element(By.CSS_SELECTOR, ".css-4rbku5:nth-child(4) > .css-1dbjc4n > .css-901oao:nth-child(1)").click()
            time.sleep(page_delay)
            self.driver.find_element(By.CSS_SELECTOR, ".css-18t94o4:nth-child(2) > .css-901oao > .css-901oao > .css-901oao").click()
            logger.info('Successfully logged out.')
        except: 
            logger.info('Not logged out correctly.')  

    def __str__(self):
        return f'Twitter Bot'

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return f'{self.subscriptions} successful new subscriptions.'

def create_list(lines):
    entries = []
    for line in lines:
        users = line.split('@')
        users.pop(0)
        [entries.append(user.replace(' ','')) for user in users]     
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
    
    # create Twitter Bot
    twitter = TwitterBot(username, password)

    try:
        # login and subscribe
        twitter.subscribe(users)
    except:
        logger.info('An error occured.')
    finally:
        twitter.driver.quit()

if __name__  == '__main__':
    main()