from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


minPrice=799       #3500.0   #Added for book for test with small price. line 113 should be 1000
maxPrice=850       #6000.0
global Test
global targetURL

global oneClickButtonActive
Test = True                  #If true program will not buy anything in last step.
oneClickButtonActive = True  # False normal way to buy.
targetURL = "https://www.amazon.com.tr/hz/wishlist/ls/KKS0SE2BHJ94/ref=nav_wishlist_lists_2?_encoding=UTF8&type=wishlist"

def Initialize():
    # options chrome userfile
    options = webdriver.ChromeOptions()
    options.add_argument(r'--user-data-dir=C:\Users\ckocoglu\PycharmProjects\MostSecretProject\ChromeUser')
    options.add_argument(r"--profile-directory=Profile 3")

    # initialize web driver
    driver = webdriver.Chrome(r"C:\Users\ckocoglu\PycharmProjects\MostSecretProject\Drivers\chromedriver.exe",options=options)
    #driver.maximize_window()
    time.sleep(2)
    driver.get(targetURL)
    CheckItemStocks(driver)

def ChooseAddress(self): # Its include 3 different function , address,paying option and submit checkout.
    try:
        print.info("Waiting for Address button...")
        WebDriverWait(self, 10).until(EC.presence_of_element_located((By.CLASS_NAME,'a-button-inner')))
        self.find_element_by_class_name("a-button-inner").click()
        print.info("Button found and clicked.")

        print.info("Waiting for shipping options.")
        #WebDriverWait(self, 10).until(EC.title_is('Teslimat Seçeneklerini Belirleyin - Amazon.com.tr Alışverişi Tamamla'))
        WebDriverWait(self, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'a-button-text')))
        self.find_element_by_class_name("a-button-text").click()
        print.info("Button found and clicked.")

        print("Waiting for payment options...")
        #WebDriverWait(self, 10).until(EC.title_is('Bir Ödeme Aracı Seç - Amazon.de Alışverişi Tamamla'))
        time.sleep(2)
        WebDriverWait(self, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'a-button-inner')))
        self.find_element_by_class_name("a-button-inner").click()
        print("Found and clicked.")
        try:
            WebDriverWait(self, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'a-button-inner')))
            self.find_element_by_class_name("a-button-inner").click()
        except:
            #WebDriverWait(self, 10).until(EC.title_is('Siparişinizi Verin - Amazon.com.tr Alışverişi Tamamla'))
            WebDriverWait(self, 10).until(EC.presence_of_element_located((By.ID, 'placeYourOrder')))
            if Test:
                print("This is a test , program will not click checkout button.")
                self.get(targetURL)
                CheckItemStocks(self)
                pass
            else:
                self.find_element_by_id("placeYourOrder").click()
                print("Order Complete.")
                print("Program starting again.")
                self.get(targetURL)
                CheckItemStocks(self)
                pass
    except:
        print("Somethings gone wrong.")

def Checkout(self):
    try:
        print("Waiting for Checkout button...")
        WebDriverWait(self, 10).until(EC.presence_of_element_located((By.LINK_TEXT,'Alışverişi tamamla')))
        self.find_element_by_link_text("Alışverişi tamamla").click()
        time.sleep(4)
        print("Button found and clicked.")
        WebDriverWait(self, 10).until(EC.title_is('Teslimat adresi seçin'))
        ChooseAddress(self)

        print(self.title)

    except:
        print("Somethings gone wrong.")


def AddToCart(self):
    self.find_element_by_link_text("Sepete Ekle").click()
    Checkout(self)

def ComparePrice(price):
    print("Checking price...")

    if(int(price)>minPrice and int(price)<maxPrice):
        print("Price is suitable.") # Go To Checkout Step
        return True
    else:
        print("Price not good")
        return False

def BuyFast(self,url):
    # Add No thanks button, if Amazon asks prime membership press No Thanks and continue process.,
    self.get(url)
    try:
        print("Waiting for Buy Now button...")
        WebDriverWait(self, 10).until(EC.presence_of_element_located((By.ID, 'buy-now-button')))
        self.find_element_by_id("buy-now-button").click()
        print("Button found and clicked.")

        if self.title == "Siparişinizi Verin - Amazon.com.tr Alışverişi Tamamla":
            WebDriverWait(self, 10).until(EC.presence_of_element_located((By.ID, 'placeYourOrder')))
            if Test:
                print("This is a test , program will not click checkout button.")
                self.get(targetURL)
                CheckItemStocks(self)
            else:
                self.find_element_by_id("placeYourOrder").click()
                time.sleep(3)
                if self.title == "Teşekkür Ederiz":
                    print("Order Complete...")
                    self.get(targetURL)
                    CheckItemStocks(self)
    except:
        print("-----------------------------------------")


def CheckItemStocks(self):
    WebDriverWait(self, 10).until(EC.title_is('Amazon.com.tr'))
    self.find_element_by_css_selector('body').send_keys(Keys.PAGE_DOWN)
    ul = self.find_element_by_id('g-items')
    lis = ul.find_elements_by_tag_name('li')
    print(len(lis))
    for li in lis:
        try:
            #print(li.find_element_by_partial_link_text("Sepete Ekle").text)
            itemID = li.get_attribute('data-itemid')
            price=float(li.find_element_by_xpath(f'//*[@id="itemPrice_{itemID}"]/span[2]/span[2]').text[0:-1])*100 #1000 olucak
            if(ComparePrice(price)):
                if oneClickButtonActive:  #Buy now button is helping us to buy fast
                    link = li.find_element_by_id(f'itemName_{itemID}').get_attribute('href')
                    BuyFast(self,link)
                else:
                    AddToCart(self)
        except:
            print("No stock")
            #pass
    self.refresh()
    CheckItemStocks(self)

Initialize();
#driver.close()


