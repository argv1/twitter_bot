from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys 
import sys
import time

class Bot():
    def __init__(self, username, password, browser, logger, page_delay):
        self.driver = webdriver.Chrome(executable_path=browser)
        self.driver.maximize_window()
        self.username = username
        self.__password = password
        self.subscriptions = 0
        self.logger = logger
        self.page_delay = page_delay
        self.logger.info('Twitter bot class created and opened chrome')
 
    def __login_to_twitter(self):
        self.logger.info('Navigating to twitter')
        try:
            self.driver.get('https://twitter.com/login')
            time.sleep(self.page_delay)

            username_field = self.driver.find_element_by_name('session[username_or_email]')
            username_field.clear()
            username_field.send_keys(self.username)
            
            password_field = self.driver.find_element_by_name('session[password]')
            password_field.clear()
            password_field.send_keys(self.__password)
            password_field.submit()
            self.logger.info('Login successful')
        
        except:
            print('Not able to login!')
            sys.exit(1)

        try:
            # Accept cookies
            self.driver.find_element(By.CSS_SELECTOR, '.css-18t94o4:nth-child(2) > .css-901oao > .css-901oao > .css-901oao').click()
            self.logger.info('Cookies accepted.')
        except: 
            self.logger.info('No cookie notification.')

    def subscribe(self, users):
        self.__login_to_twitter()

        for user in users:
            try:
                self.driver.get(f'https://twitter.com/{user}')
                time.sleep(self.page_delay)

                # check if session is still logged in or need to relogin
                elem = self.driver.find_elements(By.CSS_SELECTOR, '.r-117bsoe > .css-901oao')
                if(len(elem) > 0 and (elem[0].text == 'Etwas ist schiefgelaufen.')):
                    self.logger.info(f'Relogin required')
                    users.append(user)
                    time.sleep(120)            
                    self.__login_to_twitter()
                    continue

                # check if user exist, if not pass
                elem = self.driver.find_elements(By.CSS_SELECTOR, '.r-yfoy6g > .r-jwli3a')
                if(len(elem) > 0 and (elem[0].text == 'This account doesn’t exist' or elem[0].text == 'Dieser Account existiert nicht')):
                    self.logger.info(f'User {user}does not exist.')
                    continue

                # follow user            
                self.driver.find_element(By.CSS_SELECTOR, '.css-1dbjc4n:nth-child(1) > .css-18t94o4:nth-child(1) > .css-901oao > .css-901oao > .css-901oao').click()
                self.logger.info(f'Successful subscribed to @{user}.')
                self.subscriptions += 1
            except:   
                self.logger.info(f'Subscribtion to @{user} not possible.') 

        self.logger.info(f'Successfully subscribed to {self.subscriptions} out of {len(users)}.') 
        self.logout()

    def logout(self):
        try:
            self.driver.get("https://twitter.com/home")
            time.sleep(self.page_delay)
            self.driver.find_element(By.CSS_SELECTOR, ".r-obd0qt > .r-jwli3a").click()
            time.sleep(self.page_delay)
            self.driver.find_element(By.CSS_SELECTOR, ".css-4rbku5:nth-child(4) > .css-1dbjc4n > .css-901oao:nth-child(1)").click()
            time.sleep(self.page_delay)
            self.driver.find_element(By.CSS_SELECTOR, ".css-18t94o4:nth-child(2) > .css-901oao > .css-901oao > .css-901oao").click()
            self.logger.info('Successfully logged out.')
        except: 
            self.logger.info('Not logged out correctly.')  

    def __str__(self):
        return f'Twitter Bot'

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return f'{self.subscriptions} successful new subscriptions.'