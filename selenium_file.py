import selenium
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

list_ClassName = [
    "new-price",
    "discounted",
    "ty-plus-price-discounted-price"
]

chrome_secenekleri = Options()
chrome_secenekleri.add_argument("--headless")
chrome_secenekleri.add_argument("user-agent=...")


class FiyatTakip:
    def __init__(self):
        self.fiyat = 0
        self.durum = False
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                  options=chrome_secenekleri)

    def go_link(self,link):    # link GUI kısmından alınacak
        self.link = link
        self.driver.get(self.link)
        time.sleep(3)
        self.durum=False
        try:
            for i, class_name in enumerate(list_ClassName):
                try:
                    new_price = self.driver.find_element(By.CLASS_NAME, class_name)
                    self.fiyat = new_price.text
                    if self.fiyat != "":
                        print(f"Fiyat {i + 1 }. yöntem ile alındı = {self.fiyat}\n")
                        self.durum = True
                        return self.fiyat

                except NoSuchElementException:
                    print(f"❌ {i + 1}. yöntem ({class_name}) başarısız. Sonrakine geçiliyor...")

        except:
            print("FİYAT ALINAMDI  ")

    def fiyat_analiz(self):
        print(self.fiyat)





