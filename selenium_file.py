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




class FiyatTakip:
    def __init__(self):
        self.driver= None

    def setup_driver(self):
        chrome_secenekleri = Options()
        #chrome_secenekleri.add_argument("--headless")
        chrome_secenekleri.add_argument("--start-maximized")
        chrome_secenekleri.add_argument("--disable-notifications")
        chrome_secenekleri.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                       options=chrome_secenekleri)
    def fiyat_temizle(self, fiyat_text):
        try:
            self.temiz = fiyat_text.replace("TL", "").strip()  ## 1. 'TL' ve boşlukları sil
            self.temiz = self.temiz.replace(".", "")    ## 2. Binlik ayracı olan noktayı (.) sil -> '1250,90'
            self.temiz = self.temiz.replace(",", ".")   ## 3. Ondalık ayracı olan virgülü (,) noktaya çevir -> '1250.90'
            return float(self.temiz)
        except Exception as e:
            print(f"Dönüştürme hatası: {e}")
            return None

    def go_link(self, link):
        if self.driver is None:
            self.setup_driver()
        try:
            self.driver.get(link)
        except:
            self.setup_driver()
            self.driver.get(link)
        wait_ten_sn = WebDriverWait(self.driver, 10)
        wait_two_sn = WebDriverWait(self.driver, 2)
        # --- ADIM 1: POP-UP KAPATMA OPERASYONU ---
        try:
            popup_kapat = wait_ten_sn.until(EC.element_to_be_clickable((By.ID, "onetrust-reject-all-handler")))
            popup_kapat.click()
            print("Pop-up belası kapatıldı.")
            time.sleep(1)
            try:
                popup_kapat2 = wait_two_sn.until(EC.element_to_be_clickable((By.CLASS_NAME,"onboarding__default-renderer-primary-button")))
                popup_kapat2.click()
                print("Pop-up 2 belası kapatıldı.")
                time.sleep(1)
            except:
                print("Pop-up 2 kapatılamadı ya da bulunamadı")
        except:
            print("Pop-up çıkmadı veya kapatılamadı (Önemli değil).")

        list_ClassName = [
            (By.CLASS_NAME,"discounted"),
            (By.CLASS_NAME,"new-price"),
            (By.CLASS_NAME,"ty-plus-price-discounted-price"),
        ]

        ham_fiyat = None
        i = 1
        for tip, deger in list_ClassName:
            try:
                element = wait_two_sn.until(EC.visibility_of_element_located((tip, deger)))
                ham_fiyat = element.text
                print(f"{i}. yöntem ile Buldum! ({deger}): {ham_fiyat}")
                break
            except:
                print(f"{i}. yöntem({deger}) ile bulunamadı... ")
                i = i + 1
                continue

        if ham_fiyat:
            return self.fiyat_temizle(ham_fiyat)
        else:
            print("HATA: Hiçbir yöntemle fiyat bulunamadı. Sayfa yapısı değişmiş olabilir.")
            return None

    def kapat(self):
        if self.driver:
            self.driver.quit()

    def fiyat_analiz(self):
        print(self.temiz)




