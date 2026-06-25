#import ile Gerekli kütüphaneleri aktarıyoruz. Aynı kütüphaneleri kullandığım için sadece yenilerini açıklayacağım.
import os
import stat
import hashlib
import datetime
import tkinter as tk # tkinter: Yaptığımız proje terminalde değil de grafik arayüz (GUI)oluşturmak için kullanılan kütüphane as tk: tk olarak adlandırdım.
from tkinter import filedialog, messagebox #Tikinter kütüpanesinden filedialog,mesagebox aldık kullanıcıdan dosya alabilmem ve kullanıcıya uyarı mesajları gösterebilmem için kullandım

# --- İzin kontrol fonksiyonu ---
def izin_kontrol(dizin):
    try:
        sayac = 0  # İzinleri kontrol etmek için sayaç
        sonuc = "" #Sonuçları metin olarak biriktirmek için boş string
        # Dizin içindeki dosyaları tarıyoruz
        for kok, klasorler, dosyalar in os.walk(dizin): # os.walk: dizin içindeki tüm dosya ve klasörleri dolaşır
            for dosya in dosyalar:
                # os.path.join: Klasör yolu ile dosya adını güvenli bir şekilde birleştirerek tam dosya yolunu oluşturur.
                dosya_yolu = os.path.join(kok, dosya)
                
                # os.stat: Dosyanın boyut, değiştirilme tarihi ve izinler gibi sistem özelliklerini (meta verilerini) döndürür.
                # .st_mode: Bu özellikler içinden sadece dosya türü ve erişim izinleri (chmod) bilgilerini alır.
                kip = os.stat(dosya_yolu).st_mode
                
                # stat.S_IMODE: Dosya kipinden (st_mode) sadece erişim izinlerine ait olan bitleri ayıklar.
                # 0o777: Sekizlik (octal) sayı sisteminde tam okuma, yazma ve çalıştırma iznini (rwxrwxrwx) temsil eder.
                if stat.S_IMODE(kip) == 0o777:
                    sonuc += f"777 iznine sahip dosya: {dosya_yolu}\n"
                    sayac += 1
                    
        # Elde edilen sonuçları, toplam sayıyı ve işlemin bittiği anki güncel zamanı (datetime.now) metne ekler.
        sonuc += f"Toplam 777 iznine sahip dosya sayısı: {sayac}\nİşlem tamamlandı: {datetime.datetime.now()}\n"
        return sonuc
    except Exception as hata:
        # Kodun çalışma esnasında (örneğin yetkisiz bir klasöre erişmeye çalışırken) hata oluşursa, programın çökmesini engeller ve hatayı döndürür.
        return f"Hata oluştu: {str(hata)}"

# --- SHA256 hash fonksiyonu ---
def sifre_hash(sifre):
    try:
        # hashlib.sha256: SHA-256 algoritmasını hazırlar.
        # .encode(): String (metin) formatındaki şifreyi, hash algoritmalarının işleyebileceği 'byte' formatına çevirir.
        # .hexdigest(): Oluşturulan karmaşık hash değerini okunabilir, 16'lık (hexadecimal) tabanda bir metne dönüştürür.
        sonuc = hashlib.sha256(sifre.encode()).hexdigest()
        return f"Girilen şifrenin SHA256 hash değeri:\n{sonuc}\nİşlem tamamlandı: {datetime.datetime.now()}\n"
    except Exception as hata:
        return f"Hata oluştu: {str(hata)}"

# --- Arayüzde dizin seçme ---
def dizin_sec():
    # filedialog.askdirectory(): Kullanıcının bilgisayarından bir klasör seçebilmesi için işletim sisteminin klasör seçme penceresini açar.
    dizin = filedialog.askdirectory()
    if dizin: # Eğer kullanıcı bir klasör seçtiyse (iptal etmediyse)
        sonuc = izin_kontrol(dizin) # Seçilen klasör yolunu izin_kontrol fonksiyonuna gönderip taratır.
        
        # .delete("1.0", tk.END): Metin kutusunun ilk satırından (1.0) sonuna kadar (tk.END) olan eski yazıları temizler.
        izin_metin_kutusu.delete("1.0", tk.END)
        
        # .insert(tk.END, sonuc): Fonksiyondan gelen güncel tarama sonuçlarını metin kutusunun sonuna ekler.
        izin_metin_kutusu.insert(tk.END, sonuc)

# --- Arayüzde şifre hash hesaplama ---
def hash_hesapla():
    # .get(): Şifre giriş kutusuna (Entry) kullanıcının yazdığı metni okur.
    sifre = sifre_giris.get()
    if sifre: # Eğer kullanıcı kutuyu boş bırakmadıysa
        sonuc = sifre_hash(sifre) # Şifreyi hash fonksiyonuna gönderip sonucunu alır.
        
        # Hash metin kutusundaki eski sonuçları siler ve yeni hash değerini kutunun içine yazar.
        hash_metin_kutusu.delete("1.0", tk.END)
        hash_metin_kutusu.insert(tk.END, sonuc)
    else:
        # messagebox.showwarning: Kullanıcı şifre alanını boş bırakıp butona basarsa ekrana bir uyarı penceresi çıkartır.
        messagebox.showwarning("Uyarı", "Lütfen bir şifre girin!")

# --- Tkinter arayüzü ---
# tk.Tk(): Ana uygulama penceresini oluşturur ve başlatır.
pencere = tk.Tk()
# .title(): Pencerenin üst barında görünecek başlığı belirler.
pencere.title("Dosya İzin ve SHA256 Arayüzü")
# .geometry(): Pencerenin başlangıç genişlik ve yükseklik boyutunu piksel cinsinden (Genişlik x Yükseklik) ayarlar.
pencere.geometry("550x500")
# .configure(bg=...): Pencerenin arka plan rengini (Hex renk koduyla) değiştirir.
pencere.configure(bg="#f5f5f5")

# Yazı tipleri
# Grafik ögelerinde (Label, Button, Text) kullanılacak ortak yazı tipi (Font) ailelerini, boyutlarını ve kalınlıklarını tanımlar.
buton_yazi_tipi = ("Arial", 10, "bold")
metin_yazi_tipi = ("Consolas", 10)

# --- Birinci Buton: Dizin Seçimi ---
# tk.Button: Tıklanabilir bir buton oluşturur. İçindeki parametrelerle rengi, yazısı, kenarlık stili (relief) ayarlanır.
# command=dizin_sec: Butona tıklandığında hangi fonksiyonun çalışacağını tetikler.
dizin_sec_butonu = tk.Button(
    pencere, 
    text="Dizin Seç ve İzin Kontrolü", 
    font=buton_yazi_tipi, 
    bg="#2980b9", 
    fg="white", 
    padx=10, 
    pady=5,
    relief="groove",
    command=dizin_sec
)
# .pack(): Oluşturulan butonu pencere içine yerleştirir. 
# pady=(20, 10): Butonun üstten 20 piksel, alttan 10 piksel boşluk bırakarak hizalanmasını sağlar.
dizin_sec_butonu.pack(pady=(20, 10))  # ortada olması için

# --- Birinci Metin Kutusu ---
# tk.Text: Kullanıcıya çok satırlı çıktı göstermek veya girdi almak için geniş bir metin alanı oluşturur.
# bd=2 (border): Kenarlık kalınlığını, relief="sunken": İçeri doğru gömük görünüm stilini belirler.
izin_metin_kutusu = tk.Text(pencere, width=100, height=16, font=metin_yazi_tipi, bd=2, relief="sunken")
izin_metin_kutusu.pack(pady=10, padx=20) # Sağdan, soldan ve dikeyden boşluk bırakarak yerleştirir.

# --- İkinci satır: Şifre giriş + buton ortada olacak
# tk.Frame: Şifre kutusu ve hash butonunu aynı satırda yan yana düzgünce gruplayabilmek için görünmez bir alt panel (kutu) oluşturur.
hash_frame = tk.Frame(pencere, bg="#f5f5f5")
hash_frame.pack(pady=10)

# tk.Entry: Kullanıcının şifre gibi tek satırlık metinler girebileceği bir giriş kutusu oluşturur.
sifre_giris = tk.Entry(hash_frame, width=40, font=metin_yazi_tipi)
# side=tk.LEFT: Elemanı Frame'in içinde sola yaslayarak yan yana dizilimi sağlar.
sifre_giris.pack(side=tk.LEFT, padx=5)

# SHA256 hesaplama işlemini başlatan ikinci buton özellikleri ve tıklandığında 'hash_hesapla' fonksiyonuna yönlendirilmesi.
sha256_butonu = tk.Button(
    hash_frame, 
    text="SHA256 Hesapla", 
    font=buton_yazi_tipi, 
    bg="#2980b9", 
    fg="white", 
    padx=15, 
    pady=5,
    relief="groove",
    command=hash_hesapla
)
sha256_butonu.pack(side=tk.LEFT, padx=5)

# --- İkinci Metin Kutusu ---
# Hesaplanan SHA256 özet değerini ekranda göstermek için kullanılan daha küçük (yüksekliği 6 satır olan) metin kutusu.
hash_metin_kutusu = tk.Text(pencere, width=100, height=6, font=metin_yazi_tipi, bd=2, relief="sunken")
hash_metin_kutusu.pack(pady=(10, 20), padx=20)

# pencere.mainloop(): Programın görünür kalmasını sağlayan, kullanıcı kapatana kadar arkada sürekli çalışan sonsuz bir döngüdür (arayüzün kalbidir).
pencere.mainloop()

