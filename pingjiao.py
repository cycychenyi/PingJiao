#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import platform
import time
import requests,winreg,zipfile,re
import click as click
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options



url='https://chromedriver.storage.googleapis.com/' # chromedriver download link

def get_Chrome_version():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Google\Chrome\BLBeacon')
    version, types = winreg.QueryValueEx(key, 'version')
    return version

def get_latest_version(url):
    '''查询最新的Chromedriver版本'''
    rep = requests.get(url).text
    time_list = []                                          # 用来存放版本时间
    time_version_dict = {}                                  # 用来存放版本与时间对应关系
    result = re.compile(r'\d.*?/</a>.*?Z').findall(rep)     # 匹配文件夹（版本号）和时间
    for i in result:
        time = i[-24:-1]                                    # 提取时间
        version = re.compile(r'.*?/').findall(i)[0]         # 提取版本号
        time_version_dict[time] = version                   # 构建时间和版本号的对应关系，形成字典
        time_list.append(time)                              # 形成时间列表
    latest_version = time_version_dict[max(time_list)][:-1] # 用最大（新）时间去字典中获取最新的版本号
    return latest_version

def get_server_chrome_versions():
    '''return all versions list'''
    versionList=[]
    url="http://npm.taobao.org/mirrors/chromedriver/"
    rep = requests.get(url).text
    result = re.compile(r'\d.*?/</a>.*?Z').findall(rep)
    for i in result:                                 # 提取时间
        version = re.compile(r'.*?/').findall(i)[0]         # 提取版本号
        versionList.append(version[:-1])                  # 将所有版本存入列表
    return versionList


def download_driver(download_url):
    '''下载文件'''
    file = requests.get(download_url)
    with open("chromedriver.zip", 'wb') as zip_file:        # 保存文件到脚本所在目录
        zip_file.write(file.content)

def get_version():
    '''查询系统内的Chromedriver版本'''
    outstd2 = os.popen('.\chromedriver.exe --version').read()
    if len(outstd2) <=0:
        return "0.0"
    return outstd2.split(' ')[1]


def unzip_driver():
    '''解压Chromedriver压缩包到指定目录'''
    f = zipfile.ZipFile("chromedriver.zip",'r')
    for file in f.namelist():
        f.extract(file)

def check_update_chromedriver():
    chromeVersion=get_Chrome_version()
    chrome_main_version=int(chromeVersion.split(".")[0]) # chrome主版本号
    driverVersion=get_version()
    driver_main_version=int(driverVersion.split(".")[0]) # chromedriver主版本号
    download_url=""
    if driver_main_version!=chrome_main_version:
        print("Downloading/Updating chromedriver")
        versionList=get_server_chrome_versions()
        if chromeVersion in versionList:
            download_url=f"{url}{chromeVersion}/chromedriver_win32.zip"
        else:
            for version in versionList:
                if version.startswith(str(chrome_main_version)):
                    download_url=f"{url}{version}/chromedriver_win32.zip"
                    break
            if download_url=="":
                print("Cannot find chromedriver")

        download_driver(download_url=download_url)
        unzip_driver()
        os.remove("chromedriver.zip")
        print('Chromedriver version:', get_version())

def init_driver() -> Chrome:
    # 初始化 driver
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    if 'Windows' in platform.platform():
        executable_path = os.path.join(os.path.dirname(__file__),
                                       'chromedriver.exe')
    else:
        executable_path = os.path.join(os.path.dirname(__file__),
                                       'chromedriver')
    driver = Chrome(executable_path=executable_path, options=chrome_options)
    driver.implicitly_wait(3)
    return driver


def login(driver: Chrome, username: str, password: str) -> None:
    driver.get('http://s.ugsq.whu.edu.cn/caslogin')
    username_input = driver.find_element_by_xpath('//*[@id="username"]')
    username_input.send_keys(username)
    password_input = driver.find_element_by_xpath('//*[@id="password"]')
    password_input.send_keys(password)
    login_button = driver.find_element_by_xpath(
        '//*[@id="casLoginForm"]/p[2]/button')
    login_button.click()


def pingjia(driver: Chrome) -> None:
    # 限制不能给满分，第一个选项四星
    driver.find_element_by_xpath(
        '//div[@class="controls" and label[@class="radio"]]/label[2]').click()
    # 其他选项全部五星
    labels = driver.find_elements_by_xpath(
        '//div[@class="controls" and label[@class="radio"]]/label[1]')[1:]
    for label in labels:
        label.click()
    # 意见填无
    textarea = driver.find_element_by_xpath(
        '//*[@id="pjnr"]/li[7]/fieldset/ol/li/div[3]/div/textarea')
    textarea.send_keys('无')
    submit_button = driver.find_element_by_xpath('//*[@id="pjsubmit"]')
    submit_button.click()
    # 评教成功后关闭弹窗
    time.sleep(1)
    close_button = driver.find_element_by_xpath(
        '//*[@id="finishDlg"]/div[2]/button')
    close_button.click()


# 是否当前页面评教完成
def pingjiaed(driver: Chrome, page_pingjiaed: bool):
    kcs = driver.find_elements_by_xpath('//*[@id="pjkc"]/tr')
    page_pingjiaed = True
    for kc in kcs:
        if kc.find_element_by_xpath('td[5]').text != '已评价':
            page_pingjiaed = False
    return page_pingjiaed


def pingjia_per_page(driver: Chrome, page_pingjiaed: bool, count: int):
    kcs = driver.find_elements_by_xpath('//*[@id="pjkc"]/tr')
    page_pingjiaed = pingjiaed(driver, page_pingjiaed)  # 当前界面评教完成
    if page_pingjiaed is True:
        return page_pingjiaed, count
    # 当前界面未评教完成，从中选择一个评教
    for kc in kcs:
        if kc.find_element_by_xpath('td[5]').text == '已评价':
            continue
        kc.find_element_by_xpath('td[6]/a').click()
        pingjia(driver)
        count += 1
        break
    return page_pingjiaed, count


@click.command()
@click.option('--username', prompt='学号')
@click.option('--password', prompt='信息门户密码（默认身份证后 6 位）')
def pingjiao(username: str, password: str):
    count = 0
    page_pingjiaed = False
    rpage = 0  # 当前评教界面
    driver = init_driver()
    login(driver, username, password)
    driver.get('https://ugsqs.whu.edu.cn/studentpj')
    driver.find_element_by_xpath('//*[@id="task-list"]/li').click()
    time.sleep(3)
    while True:
        pages = driver.find_elements_by_xpath(
            '//*[@id="tb1_wrapper"]/div/ul/li/a')[1:-1]
        page = pages[rpage]
        page.click()
        time.sleep(2)
        page_pingjiaed, count = pingjia_per_page(driver, page_pingjiaed, count)
        if page_pingjiaed is True:
            rpage += 1
            page_pingjiaed = False
        if rpage + 1 > len(pages):
            break

    print(f'共评价了 {count} 门课程')
    return


if __name__ == '__main__':
    if 'Windows' in platform.platform():
        try:
            check_update_chromedriver()
        except:
            print("Cannot Download chromedriver")
    pingjiao()
