from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def checkItems():
    time.sleep(3)
    ul = driver.find_element_by_id('g-items')
    li = ul.find_elements_by_tag_name('li')

    print(len(li))
    for lis in li:
        print(lis.find_element_by_partial_link_text("Sepete Ekle").text)






#options chrome userfile
options = webdriver.ChromeOptions()
options.add_argument(r'--user-data-dir=C:\Users\ckocoglu\PycharmProjects\MostSecretProject\ChromeUser')
options.add_argument(r"--profile-directory=Profile 3")
#initialize web driver
driver = webdriver.Chrome(r"C:\Users\ckocoglu\PycharmProjects\MostSecretProject\Drivers\chromedriver.exe",options=options)
driver.maximize_window()
time.sleep(2)
targetURL = "https://www.amazon.com.tr/hz/wishlist/ls/KKS0SE2BHJ94/ref=nav_wishlist_lists_2?_encoding=UTF8&type=wishlist"
driver.get(targetURL)
driver.find_element_by_css_selector('body').send_keys(Keys.PAGE_DOWN)

time.sleep(1)
checkItems()
#driver.close()
#driver.find_element_by_link_text("Sepete Ekle").click()
# driver.refresh()

# todo
# list içinde sepete ekle ara
# bulursan fiyatı kontrol et
# fiyat uyarsa sepete ekle -> tamamla.

