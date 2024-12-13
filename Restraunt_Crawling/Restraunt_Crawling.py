from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from time import sleep
import csv

GameUrl = 'https://www.gamestop.com/stores/'
driver = webdriver.Chrome()
driver.get(GameUrl)
cityEnter = driver.find_element("id", "store-search-input")
cityEnter.send_keys('Atlanta, GA')
submitBtn = driver.find_element(By.CLASS_NAME, "btn-storelocator-search")
submitBtn.click()
sleep(30)