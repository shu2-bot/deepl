from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import time

url = 'https://www.deepl.com/ja/translator'

iptfile = input('翻訳したいファイルを選択 : ')
optfile = input('翻訳語を入力するファイルを選択 : ')

openfile1 = open(iptfile, "r", encoding='utf-8')
openfile2 = open(optfile, "a", encoding='utf-8')
options = Options()
options.add_argument('--headless')
webdriver = webdriver.Chrome("./driver/chromedriver.exe", options=options)
webdriver.get(url)   #deepl起動

while True:
    openfile_line = openfile1.readline()
    if openfile_line:
        #deepl書き込み
        webdriver.find_element_by_xpath('//*[@id="dl_translator"]/div[5]/div[2]/div[1]/div[2]/div/textarea').send_keys(openfile_line)
        time.sleep(5)
        #翻訳語が表示されるまで待機
        while webdriver.find_element_by_xpath('//*[@id="dl_translator"]/div[5]/div[2]/div[3]/div[3]/div[1]/textarea').is_displayed() ==  False:
            time.sleep(3)
        #deepl読み込み
        html = webdriver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        target_elem = soup.find(class_="lmt__translations_as_text__text_btn")
        text = target_elem.text
        #ファイルに書き込む
        openfile2.write(text + '\n')
        #翻訳文を消す
        webdriver.find_element_by_xpath('//*[@id="dl_translator"]/div[5]/div[2]/div[1]/div[2]/div/textarea').clear()
    else:
        break

webdriver.close()
openfile1.close()
openfile2.close()