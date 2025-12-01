import tkinter as tk
from selenium_file import FiyatTakip
from tkinter import messagebox

fiyat = ""

try:
    Global_bot = FiyatTakip()
except Exception as e:
    print(f"Kritik Hata: Fiyat Takip Botu başlatılamadı! {e}")
    Global_bot = None

# ----------- SELENIUM BAŞLATAN FONKSİYON -------------
def kontrol_baslat():
    link = entry_link.get()
    if not link.startswith("http"):
        messagebox.showerror("Hata", "Lütfen geçerli bir bağlantı (URL) giriniz.")
        label2.configure(text="Geçersiz Link")
        return

    label2.configure(text="LÜTFEN BEKLEYİNİZ (Tarayıcı Başlatılıyor)...", fg="red")
    window.update()

    try:
        alinan_fiyat = Global_bot.go_link(link)
        if alinan_fiyat is not None:
            label2.configure(text=f"✅ Fiyat: {alinan_fiyat}", fg="green")
        else:
            label2.configure(text="❌ Fiyat Bulunamadı", fg="orange")

    except Exception as e:
        messagebox.showerror("Kritik Hata", f"Bot çalışırken hata oluştu: {e}")
        label2.configure(text="HATA", fg="red")

# ----------- fiyat_analiz BAŞLATAN FONKSİYON -------------
def kontrol():
    Global_bot.fiyat_analiz()





# ----------- ANA PENCERE VE AYARLAR -------------
window = tk.Tk()

window.title("🛍️ Trendyol Fiyat Takip Uygulaması")
window.geometry("700x400")
window.config(padx=50, pady=50)

# ----------- Link girme alanı - GRID Kullanımı -------------
label1 = tk.Label(
    window,
    text="Fiyat Takibi Yapılacak Ürünün Linkini Giriniz:",
    font=("Arial", 12, "bold")
)

label1.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="W")

entry_link = tk.Entry(
    window,
    width=50,
    font=("Arial", 11)
)
entry_link.grid(row=1, column=0, pady=10, ipady=5, sticky="WE")

button_baslat = tk.Button(
    window,
    text="✅ Takibi Başlat",
    command=kontrol_baslat,
    bg="#4CAF50",  # Arka plan rengi (Yeşil)
    fg="white",  # Yazı rengi
    font=("Arial", 11, "bold"),
    cursor="hand2"  # Mouse imlecini değiştir
)
button_baslat.grid(row=1, column=1, padx=(20, 0), pady=10, ipady=5, sticky="E")

label2 = tk.Label(window,text=fiyat, font=("Arial", 12, "bold"))
label2.grid(row=2, column=0, columnspan=2, pady=(0, 10), sticky="W")

# ----------- Analiz Paneli  -------------






button2 = tk.Button(window,command=kontrol)
button2.grid(row=3, column=0, pady=10, ipady=5, sticky="E")


window.mainloop()