# -*- coding: utf-8 -*-
import logging
import re
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)


class wait_for_text_to_match(object):
    def __init__(self, locator, pattern):
        self.locator = locator
        self.pattern = re.compile(pattern)

    def __call__(self, driver):
        try:
            element_text = EC._find_element(
                driver, self.locator).get_attribute("value")
            print(element_text)
            return self.pattern.search(element_text)
        except StaleElementReferenceException:
            return False


def main():
    try:
        print('start...')

        delay = 10

        browser = webdriver.Chrome('webdrivers/chromedriver')
        browser.get('https://irs.thsrc.com.tw/IMINT/')

        select_start = Select(
            browser.find_element_by_name("selectStartStation"))
        select_start.select_by_value("0")  # 0 台北

        select_destination = Select(
            browser.find_element_by_name("selectDestinationStation"))
        select_destination.select_by_value("5")  # 5 台中

        # trainCon:trainRadioGroup
        # trainCon:trainRadioGroup_0
        browser.find_element_by_id("trainCon:trainRadioGroup_0").click()

        # bookingMethod
        # radio20
        # bookingMethod1
        browser.find_element_by_id("bookingMethod1").click()

        # toTimeInputField
        element_time = browser.find_element_by_id(
            "toTimeInputField")
        element_time.clear()
        element_time.send_keys("2016/05/20")

        # toTimeTable
        select_time = Select(
            browser.find_element_by_name("toTimeTable"))
        select_time.select_by_value("130P")  # 13:30

        # ticketPanel:rows:0:ticketAmount
        select_adult = Select(
            browser.find_element_by_name("ticketPanel:rows:0:ticketAmount"))
        select_adult.select_by_value("2F")

        # ticketPanel:rows:1:ticketAmount
        select_child = Select(
            browser.find_element_by_name("ticketPanel:rows:1:ticketAmount"))
        select_child.select_by_value("0H")

        # ticketPanel:rows:2:ticketAmount
        select_love = Select(
            browser.find_element_by_name("ticketPanel:rows:2:ticketAmount"))
        select_love.select_by_value("0W")

        # ticketPanel:rows:3:ticketAmount
        select_old = Select(
            browser.find_element_by_name("ticketPanel:rows:3:ticketAmount"))
        select_old.select_by_value("0E")

        # homeCaptcha:securityCode
        # BookingS1Form_homeCaptcha_passCode

        image_verify = WebDriverWait(browser, delay).until(
            EC.presence_of_element_located(
                (By.ID, "BookingS1Form_homeCaptcha_passCode"))
        )
        # image_verify = browser.find_element_by_name(
        #     "BookingS1Form_homeCaptcha_passCode")
        src = image_verify.get_attribute("src")

        # 直接key在webdriver上 當輸入完 直接繼續
        element_verify = WebDriverWait(browser, delay).until(
            wait_for_text_to_match(
                (By.NAME, "homeCaptcha:securityCode"), r"[0-9A-Z]{4}")
        )

        # 利用console輸入 anaconda console不支援
        # user_input = raw_input("security code is: ")
        # element_verify = browser.find_element_by_name(
        #     "homeCaptcha:securityCode")
        # element_verify.clear()
        # element_verify.send_keys(user_input)

        # SubmitButton
        browser.find_element_by_name("SubmitButton").click()
        browser.get_screenshot_as_file("Screenshots/1.png")

        # -------------- second page --------------

        # page load is ok!
        WebDriverWait(browser, delay).until(
            EC.presence_of_element_located((By.NAME, "TrainQueryDataViewPanel:TrainGroup")))

        span_codes = browser.find_elements_by_id("QueryCode")

        has_situation = False

        for span_code in span_codes:
            if span_code.text == "151":
                element_chkShift = span_code.find_element_by_xpath(
                    "../../td[1]/input")
                element_chkShift.click()
                has_situation = True
                break

        if not has_situation :
            raise Exception("沒有符合班次")
        else :
        	browser.get_screenshot_as_file("Screenshots/2.png")
        	browser.find_element_by_name("SubmitButton").submit()


    	# -------------- second page --------------

    	# page load is ok!
    	WebDriverWait(browser, delay).until(
            EC.presence_of_element_located((By.NAME, "idInputRadio:idNumber")))

    	# idInputRadio1
    	browser.find_element_by_id("idInputRadio1").click()

    	# idInputRadio:idNumber - idNumber
    	element_id = browser.find_element_by_id("idNumber")
        element_id.clear()
        element_id.send_keys("N124885927")

    	# mobileInputRadio
    	browser.find_element_by_id("mobileInputRadio").click()

    	# eaiPhoneCon:phoneInputRadio:mobilePhone - mobilePhone
    	element_mobile = browser.find_element_by_id("mobilePhone")
        element_mobile.clear()
        element_mobile.send_keys("0911757685")

    	# email
    	element_email = browser.find_element_by_name("email")
        element_email.clear()
        element_email.send_keys("steny138@gmail.com")

    	# agree
    	browser.find_element_by_name("agree").click()

    	# send 
    	browser.get_screenshot_as_file("Screenshots/3.png")

    except Exception, e:
        print(e)
    finally:
        browser.close()
        # browser.quit()

    print('end...')

if __name__ == '__main__':
    main()
