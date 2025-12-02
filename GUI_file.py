import tkinter as tk
from tkinter import messagebox, ttk
from selenium_file import FiyatTakip
import time

global durum
takip_ediliyor = False

try:
    Global_bot = FiyatTakip()
except Exception as e:
    print(f"Kritik Hata: Fiyat Takip Botu başlatılamadı! {e}")
    Global_bot = None


# ----------- SELENIUM BAŞLATAN FONKSİYON -------------
def kontrol_baslat():
    global durum
    durum = False
    link = entry_link.get()
    if not link.startswith("http"):
        messagebox.showerror("Hata", "Lütfen geçerli bir bağlantı (URL) giriniz.")
        label_durum.configure(text="❌ Geçersiz Link", foreground="#e74c3c")
        return

    label_durum.configure(text="⏳ Lütfen Bekleyiniz (Tarayıcı Başlatılıyor)...", foreground="#f39c12")
    button_baslat.configure(state="disabled")
    window.update()

    try:
        alinan_fiyat = Global_bot.go_link(link)
        if alinan_fiyat is not None:
            durum = True
            label_durum.configure(text=f"✅ Fiyat Başarıyla Alındı: {alinan_fiyat}", foreground="#27ae60")
            analiz_frame.pack(pady=20, padx=20, fill="both", expand=True)
        else:
            label_durum.configure(text="❌ Fiyat Bulunamadı", foreground="#e67e22")

    except Exception as e:
        messagebox.showerror("Kritik Hata", f"Bot çalışırken hata oluştu: {e}")
        label_durum.configure(text="❌ HATA", foreground="#e74c3c")

    button_baslat.configure(state="normal")

# ----------- Kontrol DURDURMA FONKSİYON -------------
def durdur():
    global takip_ediliyor
    takip_ediliyor = False  # Döngüyü kırar
    button_durdur.pack_forget()
    button_takip.configure(state="normal", text="🚀 Takip Motorunu Başlat")
    messagebox.showinfo("Bilgi", "Takip durduruldu.")

# ----------- fiyat_analiz BAŞLATAN FONKSİYON -------------
def kontrol():
    global durum, takip_ediliyor
    takip_ediliyor = True
    button_takip.configure(state="disabled", text="⏳ Takip Çalışıyor...")
    button_durdur.pack(pady=(5, 0))
    try:
        hedef_fiyat = int(entry_hedef_fiyat.get())
        email = entry_email.get()
        sifre = entry_guvenlik_password.get()
        link = entry_link.get()  # Linki de tekrar alalım, belki değişti
    except ValueError:
        messagebox.showwarning("Hata", "Hedef fiyat sayı olmalıdır!")
        takip_ediliyor = False
        button_takip.configure(state="normal", text="🚀 Takip Motorunu Başlat")
        return

    if not hedef_fiyat or not email or not sifre:
        messagebox.showwarning("Uyarı", "Lütfen tüm alanları doldurunuz!")
        takip_ediliyor = False
        button_takip.configure(state="normal", text="🚀 Takip Motorunu Başlat")
        return

    # --- İŞLEM YAP ---
    try:
        Global_bot.go_link(link)
        # Analiz et ve mail at
        Global_bot.fiyat_analiz(email, hedef_fiyat, sifre)
        print(f"Kontrol yapıldı. Saat: {time.strftime('%H:%M:%S')}")

    except Exception as e:
        print(f"Hata: {e}")

    if takip_ediliyor:
        window.after(600000, kontrol)


# ----------- ANA PENCERE VE AYARLAR -------------
window = tk.Tk()
window.title("🛍️ Trendyol Fiyat Takip Sistemi")
window.geometry("650x800")
window.configure(bg="#ecf0f1")
window.resizable(False, False)

# Başlık Frame
header_frame = tk.Frame(window, bg="#3498db", height=80)
header_frame.pack(fill="x")

label_baslik = tk.Label(
    header_frame,
    text="🛍️ Trendyol Fiyat Takip Sistemi",
    font=("Segoe UI", 20, "bold"),
    bg="#3498db",
    fg="white"
)
label_baslik.pack(pady=20)

# Ana İçerik Frame
main_frame = tk.Frame(window, bg="#ecf0f1")
main_frame.pack(pady=20, padx=30, fill="both", expand=True)

# Link Girme Bölümü
link_frame = tk.LabelFrame(
    main_frame,
    text="📌 Ürün Linki",
    font=("Segoe UI", 12, "bold"),
    bg="#ecf0f1",
    fg="#2c3e50",
    padx=20,
    pady=15
)
link_frame.pack(fill="x", pady=(0, 15))

label_aciklama = tk.Label(
    link_frame,
    text="Takip etmek istediğiniz ürünün Trendyol linkini aşağıya yapıştırın:",
    font=("Segoe UI", 10),
    bg="#ecf0f1",
    fg="#34495e"
)
label_aciklama.pack(anchor="w", pady=(0, 10))

entry_link = tk.Entry(
    link_frame,
    font=("Segoe UI", 11),
    relief="solid",
    borderwidth=1
)
entry_link.pack(fill="x", ipady=8, pady=(0, 10))

button_baslat = tk.Button(
    link_frame,
    text="✅ Takibi Başlat",
    command=kontrol_baslat,
    bg="#27ae60",
    fg="white",
    font=("Segoe UI", 11, "bold"),
    cursor="hand2",
    relief="flat",
    padx=20,
    pady=8
)
button_baslat.pack()

# Durum Label
label_durum = tk.Label(
    main_frame,
    text="",
    font=("Segoe UI", 11, "bold"),
    bg="#ecf0f1"
)
label_durum.pack(pady=10)

# ----------- Analiz Paneli -------------
analiz_frame = tk.LabelFrame(
    main_frame,
    text="⚙️ Takip Ayarları",
    font=("Segoe UI", 12, "bold"),
    bg="#ecf0f1",
    fg="#2c3e50",
    padx=25,
    pady=20
)

# Hedef Fiyat
hedef_frame = tk.Frame(analiz_frame, bg="#ecf0f1")
hedef_frame.pack(fill="x", pady=10)

label_hedef = tk.Label(
    hedef_frame,
    text="💰 Hedef Fiyat:",
    font=("Segoe UI", 11),
    bg="#ecf0f1",
    fg="#2c3e50",
    width=20,
    anchor="w"
)
label_hedef.pack(side="left")

entry_hedef_fiyat = tk.Entry(
    hedef_frame,
    font=("Segoe UI", 11),
    relief="solid",
    borderwidth=1
)
entry_hedef_fiyat.pack(side="left", fill="x", expand=True, ipady=5)

# Email
email_frame = tk.Frame(analiz_frame, bg="#ecf0f1")
email_frame.pack(fill="x", pady=10)

label_email = tk.Label(
    email_frame,
    text="📧 E-mail Adresi:",
    font=("Segoe UI", 11),
    bg="#ecf0f1",
    fg="#2c3e50",
    width=20,
    anchor="w"
)
label_email.pack(side="left")

entry_email = tk.Entry(
    email_frame,
    font=("Segoe UI", 11),
    relief="solid",
    borderwidth=1
)
entry_email.pack(side="left", fill="x", expand=True, ipady=5)

# Güvenlik Şifresi
sifre_frame = tk.Frame(analiz_frame, bg="#ecf0f1")
sifre_frame.pack(fill="x", pady=10)

label_sifre = tk.Label(
    sifre_frame,
    text="🔒 Güvenlik Şifresi:",
    font=("Segoe UI", 11),
    bg="#ecf0f1",
    fg="#2c3e50",
    width=20,
    anchor="w"
)
label_sifre.pack(side="left")

entry_guvenlik_password = tk.Entry(
    sifre_frame,
    font=("Segoe UI", 11),
    relief="solid",
    borderwidth=1,
    show="●"
)
entry_guvenlik_password.pack(side="left", fill="x", expand=True, ipady=5)

# Bilgi Notu
bilgi_label = tk.Label(
    analiz_frame,
    text="ℹ️ Ürün fiyatı hedef fiyata ulaştığında e-mail adresinize bildirim gönderilecektir.",
    font=("Segoe UI", 9, "italic"),
    bg="#ecf0f1",
    fg="#7f8c8d",
    wraplength=450,
    justify="left"
)
bilgi_label.pack(pady=(15, 10))

# Takip Başlat Butonu
button_takip = tk.Button(
    analiz_frame,
    text="🚀 Takip Motorunu Başlat",
    command=kontrol,
    bg="#3498db",
    fg="white",
    font=("Segoe UI", 12, "bold"),
    cursor="hand2",
    relief="flat",
    padx=30,
    pady=10
)
button_takip.pack(pady=(10, 0))

button_durdur = tk.Button(
    analiz_frame,
    text="🛑 Takibi Durdur",
    command=durdur,
    bg="#c0392b",
    fg="white",
    font=("Segoe UI", 12, "bold"),
    cursor="hand2",
    relief="flat",
    padx=50,
    pady=10
)

analiz_frame.place_forget()

# Footer
footer_label = tk.Label(
    window,
    text="© 2024 Trendyol Fiyat Takip Sistemi | Geliştirildi ❤️ ile",
    font=("Segoe UI", 9),
    bg="#ecf0f1",
    fg="#95a5a6"
)
footer_label.pack(side="bottom", pady=10)

window.mainloop()