from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import configparser
from fbchat import Client
from fbchat.models import *
import logging


browser = webdriver.Chrome()
config = configparser.ConfigParser()
config.read('config.ini')
alert_user = False

#Login
browser.get('http://www.cardsphere.com/login')

username = browser.find_element_by_name('email')
username.send_keys(config['cardsphere']['username'])

password = browser.find_element_by_name('password')
password.send_keys(config['cardsphere']['password'] + Keys.RETURN)

#Get packages
browser.get('http://www.cardsphere.com/send')

wait = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "message")))

trades = browser.find_elements_by_class_name('package-heading')

for x in trades:
    print('In a package')
    values = x.find_elements_by_class_name('with-bg')
    trade_string = ""

    for index, value in enumerate(values):
        text = value.text
        trade_string += text
        trade_string += " "
        if(index == 3):
            trade_amount = float(text.replace('$', ''))
            print('trade_amount = ' + str(trade_amount))
        
    print(trade_string)
    if(trade_amount >= float(config['cardsphere']['package_value'])):
        alert_user = True
        break

#send facebook message
if(alert_user == True):
    #browser.get('http://www.facebook.com/')
    fuser = config['facebook']['username']
    fpass = config['facebook']['password']
    client = Client(fuser, fpass, user_agent="Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko")
    client.send(Message(text=trade_string), thread_id=config['facebook']['message_id'], thread_type=ThreadType.USER)
    client.logout()

browser.quit()