from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import configparser

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

#loaded = browser.find_element_by_class_name('cs-row packages')

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
    browser.get('http://www.facebook.com/')



#browser.quit()