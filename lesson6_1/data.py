import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from datetime import datetime
import csv



def getData(stock_number):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.set_window_position(x=-10000, y=-10000)
    driver.delete_all_cookies()
    url = "https://mis.twse.com.tw/stock/fibest.jsp?stock=" + stock_number

    try:
        if driver.current_url == url:
            driver.refresh()
        else:
            driver.get(url)
    except Exception as e:
        print(f"伺服器發生錯誤:{e}")
        raise Exception()

    time.sleep(2)
    driver.find_element(By.ID,"btnChangeToOdd").click()
    time.sleep(8)
    now  = datetime.now()
    now_str = now.strftime("%Y-%m-%d ")
    soup = BeautifulSoup(driver.page_source,'html.parser')

    title = soup.find(id=stock_number+"_n",class_="title").string
    if title == "-":
        title=""

    t_odd = soup.find(id=stock_number+"_t_odd", class_="oddObj").string
    if t_odd == "-":
        t_odd = ''
    else:
        t_odd =  now_str + t_odd

    odd = soup.find(id=stock_number+"_z_odd", class_="oddObj").string
    try:
        odd = float(odd)
    except:
        odd = ''

    diff_odd = soup.find(id=stock_number + "_diff_odd").string
    try:
        diff_odd = float(diff_odd[1:])
    except:
        diff_odd = ''

    percent_diff = soup.find(id=stock_number + "_pre_odd").string
    try:
        percent_diff = float(percent_diff[1:-3])
    except:
        percent_diff = ''


    driver.quit()

    return [title,t_odd,odd,diff_odd,percent_diff]

while True:
    dataList = getData("2330")
    if not ('' in dataList):
        if not os.path.isdir('assets'):
            os.mkdir('assets')

        now = datetime.now()
        now_str = now.strftime("%Y-%m-%d.csv")
        abs_file_name = os.path.abspath('./assets/'+now_str)
        with open(abs_file_name, 'a', encoding='utf-8',newline='') as file:
            writer = csv.writer(file,delimiter=',')
            writer.writerow(dataList)







'''
if not os.path.isdir('assets'):
    os.mkdir('assets')

abs_file_name = os.path.abspath('./assets/oop.txt')
file  = open(abs_file_name,'w',encoding='utf-8')
print("Hello! Python!",file=file)
file.close()
'''