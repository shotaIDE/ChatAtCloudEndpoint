# coding: utf-8
import argparse
import json
from time import sleep

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

TIMEOUT_SEC = 30

def find_room(send_room_name: str):
    room_name_elements = browser.find_elements_by_xpath(
    '//*[contains(@class,\'room_name_content\')]')

    for room_name_element in room_name_elements:
        room_name = room_name_element.text

        if room_name == send_room_name:
            return room_name_element

    browser.find_element_by_id(
        'room_search_box_content').send_keys(send_room_name)

    for count in range(5):
        sleep(1)

        room_name_elements = browser.find_elements_by_xpath(
            '//*[contains(@class,\'room_name_content\')]')

        for room_name_element in room_name_elements:
            room_name = room_name_element.text

            if room_name == send_room_name:
                return room_name_element

parser = argparse.ArgumentParser()
parser.add_argument('--prod', action='store_true', default=False)
parser.add_argument('--suffix', type=str, default=None)
parser.add_argument('--file', type=str, default=None)
arguments = parser.parse_args()

is_debug = not arguments.prod
send_message_suffix = arguments.suffix

if send_message_suffix is None:
    send_message_suffix_file = arguments.file
    with open(send_message_suffix_file, 'r', encoding='utf8') as f:
        send_message_suffix_list = f.readlines()
        send_message_suffix = ''.join(send_message_suffix_list)

with open('settings.json', 'r', encoding='utf8') as f:
    settings = json.load(f)

chrome_driver_path = settings['chromeDriverPath']
user_ID = settings['userID']
password = settings['password']
sign_on_url = settings['signOnUrl']
send_room_name = settings['roomName']
send_message_prefix = settings['messagePrefix']

options = Options()
browser = webdriver.Chrome(executable_path=chrome_driver_path, options=options)
browser.get(sign_on_url)

WebDriverWait(browser, TIMEOUT_SEC).until(
    EC.presence_of_element_located((By.ID, 'username')))
browser.find_element_by_id('username').send_keys(user_ID)
browser.find_element_by_id('password').send_keys(password)

browser.find_element_by_link_text('Sign On').click()

WebDriverWait(browser, TIMEOUT_SEC).until(
    EC.presence_of_element_located(
        (By.XPATH, '//*[contains(@class,\'room_name_content\')]')))

room_name_element = find_room(send_room_name=send_room_name)

room_name_elements = browser.find_elements_by_xpath(
    '//*[contains(@class,\'room_name_content\')]')

for room_name_element in room_name_elements:
    room_name = room_name_element.text

    if room_name != send_room_name:
        continue

    room_name_element.click()

    WebDriverWait(browser, TIMEOUT_SEC).until(
        EC.presence_of_element_located((By.ID, 'input_msg')))
    browser.find_element_by_id('input_msg').send_keys(
        f'{send_message_prefix}{send_message_suffix}')

    send_button = browser.find_element_by_id('send_btn')
    if not is_debug:
        send_button.click()

    sleep(3)
    break

browser.quit()
