#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import platform
import time

import click as click
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options


def init_driver() -> Chrome:
    # 初始化 driver
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    if 'Windows' in platform.platform():
        executable_path = os.path.join(os.path.dirname(__file__), 'chromedriver.exe')
    else:
        executable_path = os.path.join(os.path.dirname(__file__), 'chromedriver')
    driver = Chrome(executable_path=executable_path, options=chrome_options)
    driver.implicitly_wait(3)
    return driver


def login(driver: Chrome, username: str, password: str) -> None:
    driver.get('http://s.ugsq.whu.edu.cn/caslogin')
    username_input = driver.find_element_by_xpath('//*[@id="username"]')
    username_input.send_keys(username)
    password_input = driver.find_element_by_xpath('//*[@id="password"]')
    password_input.send_keys(password)
    time.sleep(10)
    #login_button = driver.find_element_by_xpath('//*[@id="casLoginForm"]/p[5]/button')
    #login_button.click()

def pingjia(driver: Chrome) -> None:
    # 限制不能给满分，第一个选项四星
    driver.find_element_by_xpath('//div[@class="controls" and label[@class="radio"]]/label[2]').click()
    # 其他选项全部五星
    labels = driver.find_elements_by_xpath('//div[@class="controls" and label[@class="radio"]]/label[1]')[1:]
    for label in labels:
        label.click()
    # 意见填无
    textarea = driver.find_element_by_xpath('//*[@id="pjnr"]/li[7]/fieldset/ol/li/div[3]/div/textarea')
    textarea.send_keys('无')
    submit_button = driver.find_element_by_xpath('//*[@id="pjsubmit"]')
    submit_button.click()
    # 评教成功后关闭弹窗
    close_button = driver.find_element_by_xpath('//*[@id="finishDlg"]/div[2]/button')
    close_button.click()


def pingjia_per_page(driver: Chrome, all_pingjiaed: bool, count: int) -> tuple:
    kcs = driver.find_elements_by_xpath('//*[@id="pjkc"]/tr')
    for kc in kcs:
        if not all_pingjiaed:
            break
        if kc.find_element_by_xpath('td[5]').text == '已评价':
            continue
        kc.find_element_by_xpath('td[6]/a').click()
        pingjia(driver)
        all_pingjiaed = False
        count += 1
        time.sleep(3)
    return count, all_pingjiaed


@click.command()
@click.option('--username', prompt='学号')
@click.option('--password', prompt='信息门户密码（默认身份证后 6 位）')
def pingjiao(username: str, password: str) -> int:
    count = 0
    driver = init_driver()
    login(driver, username, password)
    all_pingjiaed = False

    while not all_pingjiaed:
        all_pingjiaed = True
        driver.get('http://s.ugsq.whu.edu.cn/studentpj')
        driver.find_element_by_xpath('//*[@id="task-list"]/li').click()
        # 首页
        count, all_pingjiaed = pingjia_per_page(driver, all_pingjiaed, count)
        if not all_pingjiaed:
            continue
        print("Entering Remain")  # 更新all_pingjiaed flag
        # 剩余页
        pages = driver.find_elements_by_xpath('//*[@id="tb1_wrapper"]/div/ul/li/a')[2:-1]
        for page in pages:
            if not all_pingjiaed:
                break
            page.click()
            time.sleep(3)
            count,all_pingjiaed = pingjia_per_page(driver, all_pingjiaed, count)

    print(f'共评价了 {count} 门课程')
    return count


if __name__ == '__main__':
    pingjiao()
