import datetime
import json
import os
import sys
import time

import requests
from selenium import webdriver
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

SELENIUM_HUB_HOST = os.environ["SELENIUM_HUB_HOST"]
SELENIUM_HUB_PORT = int(os.environ["SELENIUM_HUB_PORT"])
HUBURL = f"http://{SELENIUM_HUB_HOST}:{SELENIUM_HUB_PORT}/wd/hub"
WEB_HOST = os.environ["WEB_HOST"]
WEB_PORT = int(os.environ["WEB_PORT"])
WEBURL = f"http://{WEB_HOST}:{WEB_PORT}/"
APIURL = WEBURL + "api/v1"

##################
### GET BUTTON ###
##################


def test_get_success_nokey():
    print("test_get_success_nokey started")
    clean_and_add_keys()
    try:
        (driver, elems) = get_driver_elements()
        elems["get-button"].click()
        time.sleep(1)
        test_name = sys._getframe().f_code.co_name
        take_screenshot(driver, test_name)
        assert elems["request-url"].text == "/api/v1/keys/"
        assert elems["request-body"].text == ""
        assert elems["response-code"].text == "200"
        rbody = json.loads(elems["response-body"].text)
        assert rbody == {"apple": "red", "banana": "yellow"}
        driver.quit()
    except:
        driver.quit()
        raise


def test_get_success_keyexist():
    print("test_get_success_keyexist started")
    clean_and_add_keys()
    try:
        (driver, elems) = get_driver_elements()
        elems["key"].send_keys("apple")
        elems["get-button"].click()
        time.sleep(1)
        take_screenshot(driver, sys._getframe().f_code.co_name)
        assert elems["request-url"].text == "/api/v1/keys/apple"
        assert elems["request-body"].text == ""
        assert elems["response-code"].text == "200"
        rbody = json.loads(elems["response-body"].text)
        assert rbody == {"apple": "red"}
        driver.quit()
    except:
        driver.quit()
        raise


def test_get_fail_keynotexist():
    print("test_get_fail_keynotexist started")
    clean_and_add_keys()
    try:
        (driver, elems) = get_driver_elements()
        elems["key"].send_keys("grape")
        elems["get-button"].click()
        time.sleep(1)
        take_screenshot(driver, sys._getframe().f_code.co_name)
        assert elems["request-url"].text == "/api/v1/keys/grape"
        assert elems["request-body"].text == ""
        assert elems["response-code"].text == "404"
        rbody = json.loads(elems["response-body"].text)
        assert rbody["code"] == 404
        driver.quit()
    except:
        driver.quit()
        raise


###################
### POST BUTTON ###
###################


def test_post_success():
    print("test_post_success started")
    clean_and_add_keys()
    try:
        (driver, elems) = get_driver_elements()
        elems["key"].send_keys("grape")
        elems["value"].send_keys("purple")
        elems["post-button"].click()
        time.sleep(1)
        take_screenshot(driver, sys._getframe().f_code.co_name)
        assert elems["request-url"].text == "/api/v1/keys/grape"
        assert elems["request-body"].text == "purple"
        assert elems["response-code"].text == "200"
        rbody = json.loads(elems["response-body"].text)
        assert rbody == {"grape": "purple"}
        driver.quit()
    except:
        driver.quit()
        raise


def test_post_fail_nokey():
    print("test_post_fail_nokey started")
    clean_and_add_keys()
    try:
        (driver, elems) = get_driver_elements()
        elems["value"].send_keys("purple")
        elems["post-button"].click()
        time.sleep(1)
        take_screenshot(driver, sys._getframe().f_code.co_name)
        assert elems["request-url"].text == "/api/v1/keys/"
        assert elems["request-body"].text == "purple"
        assert elems["response-code"].text == "405"
        rbody = json.loads(elems["response-body"].text)
        assert rbody["code"] == 405
        driver.quit()
    except:
        driver.quit()
        raise


def test_post_fail_novalue():
    print("test_post_fail_novalue started")
    clean_and_add_keys()
    try:
        (driver, elems) = get_driver_elements()
        elems["key"].send_keys("grape")
        elems["post-button"].click()
        time.sleep(1)
        take_screenshot(driver, sys._getframe().f_code.co_name)
        assert elems["request-url"].text == "/api/v1/keys/grape"
        assert elems["request-body"].text == ""
        assert elems["response-code"].text == "400"
        rbody = json.loads(elems["response-body"].text)
        assert rbody["code"] == 400
        driver.quit()
    except:
        driver.quit()
        raise


def test_post_fail_keyexist():
    print("test_post_fail_keyexist started")
    clean_and_add_keys()
    try:
        (driver, elems) = get_driver_elements()
        elems["key"].send_keys("apple")
        elems["value"].send_keys("green")
        elems["post-button"].click()
        time.sleep(1)
        take_screenshot(driver, sys._getframe().f_code.co_name)
        assert elems["request-url"].text == "/api/v1/keys/apple"
        assert elems["request-body"].text == "green"
        assert elems["response-code"].text == "409"
        rbody = json.loads(elems["response-body"].text)
        assert rbody["code"] == 409
        driver.quit()
    except:
        driver.quit()
        raise


##################
### PUT BUTTON ###
##################


def test_put_success_create():
    print("test_put_success_create started")
    clean_and_add_keys()
    try:
        (driver, elems) = get_driver_elements()
        elems["key"].send_keys("grape")
        elems["value"].send_keys("purple")
        elems["put-button"].click()
        time.sleep(1)
        take_screenshot(driver, sys._getframe().f_code.co_name)
        assert elems["request-url"].text == "/api/v1/keys/grape"
        assert elems["request-body"].text == "purple"
        assert elems["response-code"].text == "200"
        rbody = json.loads(elems["response-body"].text)
        assert rbody == {"grape": "purple"}
        driver.quit()
    except:
        driver.quit()
        raise


def test_put_success_update():
    print("test_put_success_update started")
    clean_and_add_keys()
    try:
        (driver, elems) = get_driver_elements()
        elems["key"].send_keys("apple")
        elems["value"].send_keys("green")
        elems["put-button"].click()
        time.sleep(1)
        take_screenshot(driver, sys._getframe().f_code.co_name)
        assert elems["request-url"].text == "/api/v1/keys/apple"
        assert elems["request-body"].text == "green"
        assert elems["response-code"].text == "200"
        rbody = json.loads(elems["response-body"].text)
        assert rbody == {"apple": "green"}
        driver.quit()
    except:
        driver.quit()
        raise


def test_put_fail_nokey():
    print("test_put_fail_nokey started")
    clean_and_add_keys()
    try:
        (driver, elems) = get_driver_elements()
        elems["value"].send_keys("purple")
        elems["put-button"].click()
        time.sleep(1)
        take_screenshot(driver, sys._getframe().f_code.co_name)
        assert elems["request-url"].text == "/api/v1/keys/"
        assert elems["request-body"].text == "purple"
        assert elems["response-code"].text == "405"
        rbody = json.loads(elems["response-body"].text)
        assert rbody["code"] == 405
        driver.quit()
    except:
        driver.quit()
        raise


def test_put_fail_novalue():
    print("test_put_fail_novalue started")
    clean_and_add_keys()
    try:
        (driver, elems) = get_driver_elements()
        elems["key"].send_keys("grape")
        elems["put-button"].click()
        time.sleep(1)
        take_screenshot(driver, sys._getframe().f_code.co_name)
        assert elems["request-url"].text == "/api/v1/keys/grape"
        assert elems["request-body"].text == ""
        assert elems["response-code"].text == "400"
        rbody = json.loads(elems["response-body"].text)
        assert rbody["code"] == 400
        driver.quit()
    except:
        driver.quit()
        raise


#####################
### DELETE BUTTON ###
#####################


def test_delete_success():
    print("test_delete_success started")
    clean_and_add_keys()
    try:
        (driver, elems) = get_driver_elements()
        elems["key"].send_keys("apple")
        elems["delete-button"].click()
        time.sleep(1)
        take_screenshot(driver, sys._getframe().f_code.co_name)
        assert elems["request-url"].text == "/api/v1/keys/apple"
        assert elems["request-body"].text == ""
        assert elems["response-code"].text == "200"
        rbody = json.loads(elems["response-body"].text)
        assert rbody == {}
        driver.quit()
    except:
        driver.quit()
        raise


def test_delete_fail_nokey():
    print("test_delete_fail_nokey started")
    clean_and_add_keys()
    try:
        (driver, elems) = get_driver_elements()
        elems["delete-button"].click()
        time.sleep(1)
        take_screenshot(driver, sys._getframe().f_code.co_name)
        assert elems["request-url"].text == "/api/v1/keys/"
        assert elems["request-body"].text == ""
        assert elems["response-code"].text == "405"
        rbody = json.loads(elems["response-body"].text)
        assert rbody["code"] == 405
        driver.quit()
    except:
        driver.quit()
        raise


def test_delete_fail_keynotexist():
    print("test_delete_fail_keynotexist started")
    clean_and_add_keys()
    try:
        (driver, elems) = get_driver_elements()
        elems["key"].send_keys("purple")
        elems["delete-button"].click()
        time.sleep(1)
        take_screenshot(driver, sys._getframe().f_code.co_name)
        assert elems["request-url"].text == "/api/v1/keys/purple"
        assert elems["request-body"].text == ""
        assert elems["response-code"].text == "404"
        rbody = json.loads(elems["response-body"].text)
        assert rbody["code"] == 404
        driver.quit()
    except:
        driver.quit()
        raise


###############
### Utility ###
###############

# print(driver.find_element_by_id('table').get_attribute('innerHTML'))


def get_driver_elements():
    print("get_driver_elements started")
    options = webdriver.ChromeOptions()
    print("start options.add_argument('--headless')")
    options.add_argument("--headless")
    print("start driver = webdriver.Remote(")
    driver = webdriver.Remote(
        command_executor=HUBURL,
        options=options,
    )
    print("start driver.get(WEBURL)")
    driver.get(WEBURL)
    elements = {}
    for html_id in [
        "key",
        "value",
        "get-button",
        "post-button",
        "put-button",
        "delete-button",
        "request-url",
        "request-body",
        "response-code",
        "response-body",
    ]:
        print("start driver.find_element_by_id(html_id)")
        elements[html_id] = driver.find_element_by_id(html_id)
    print(f"elements: {elements}")
    return (driver, elements)


def take_screenshot(driver, title):
    print("take_screenshot started")
    today = datetime.datetime.today()
    timestamp = today.strftime("%Y%m%d%H%M%S")
    driver.save_screenshot(f"/images/{timestamp}-{title}.png")


def clean():
    print("clean started")
    r = requests.get(f"{APIURL}/keys/")
    for key in r.json():
        requests.delete(f"{APIURL}/keys/{key}")
    num_keys = len(requests.get(f"{APIURL}/keys/").json())
    assert 0 == num_keys


def clean_and_add_keys():
    print("clean_and_add_keys started")
    clean()
    r = requests.put(f"{APIURL}/keys/apple", data="red")
    assert r.status_code == 200
    r = requests.put(f"{APIURL}/keys/banana", data="yellow")
    assert r.status_code == 200
