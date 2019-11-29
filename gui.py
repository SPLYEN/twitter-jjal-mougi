from tkinter import *

import time

import requests

from selenium import webdriver

from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup

window=Tk()

label=Label(window, text='트위터 짤 모으기')
entry1=Entry(window)
entry2=Entry(window)
b1=Label(window, text='다운로드 경로')
b2=Button(window, text='다운로드 시작')

label.grid(row=0, column=0, sticky='ew')
entry1.grid(row=1, column=0)
entry2.grid(row=2, column=0)
b1.grid(row=1, column=1)
b2.grid(row=2, column=1)


def downloadpath(event):
    return entry1.get()

b1.bind('<Button-1>', downloadpath)


def downloadstart(event):
    path=entry1.get()

    options = webdriver.ChromeOptions()

    options.add_argument('headless')

    options.add_argument('window-size=1920x1080')

    options.add_argument("disable-gpu")

    options.add_argument(
        "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36")

    browser = webdriver.Chrome(r'C:\Users\Family\Downloads\chromedriver_win32\chromedriver.exe', chrome_options=options)

    url = 'https://twitter.com/'+entry2.get()
    body = browser.find_element_by_tag_name('body')

    browser.get(url)
    time.sleep(1)

    while True:
        lastHeight = browser.execute_script("return document.body.scrollHeight")

        browser.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(1)

        newHeight = browser.execute_script("return document.body.scrollHeight")
        print(newHeight)

        if newHeight != lastHeight:
            lastHeight = newHeight
        else:
            break

    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')
    imgs = soup.find_all('div', class_="AdaptiveMedia-photoContainer")

    for img in imgs:
        link = img.get('data-image-url')
        pic_res = requests.request("GET", link).content
        time.sleep(0.5)
        name = link[link.rfind('/') + 1:]
        with open(path +'/'+ name, 'wb') as f:
            f.write(pic_res)
        f.close()
        print(name)

b2.bind('<Button-1>', downloadstart)




window.mainloop()


