#programlama ödevi: IP checker(Kullanıcının verdiği IP adresi kontrol eder.)
#import: Hazır bir kütüphaneye çağırmak için kullanılır.
import tkinter as tk   # tkinter: Yaptığımız proje terminalde değil de grafik arayüz (GUI)oluşturmak için kullanılan kütüphane as tk: tk olarak adlandırdım.
import platform        # platform: Programın çalıştığı işletim sistemin bilgileri öğrenmek için kullanır(Windows/Linux/Mac)
import subprocess      # subprocess: Sistem komutlarını (ping vb.) çalıştırmak için kullanılır
import ipaddress       # ipaddress: IP adreslerinin geçerli olup olmadığını kontrol etmek için kullanılır
#programın 

def ip_normalizasyon(ip):   # Fonksiyonun başlanması Bu fonksiyon IP adreslerin doğruluyor
    parcalar = ip.split(".")   # IP'yi noktalarına ayırır
    temiz_parcalar = []        # Temizlenmiş parçaları tutacak liste
    for p in parcalar:         # Her parçayı tek tek kontrol eder
        if p.isdigit():        # Eğer parça sadece rakamlardan oluşuyorsa
            temiz_parcalar.append(str(int(p))) # int() Baştaki sıfırları kaldırır ör: 02=2
        else:
            temiz_parcalar.append(p)            # rakam değilse olduğu gibi ekler
    return ".".join(temiz_parcalar)             # parçaları tekrar birleştirip IP'yi döndürür

# Bu fonksiyon programın ana fonkisyonu kullanıcının girdiği IP adresini alarak doğruluğunu kontrol ederek aktif olup olmadığını anlamak için ona "Ping" atar.
def ip_kontrol(etkinlik=None):   # ip_kontrol: IP kontrolünü yapan fonksiyon (Enter tuşu ile işlem yapmak için etkinlik=None)
    ip = giris_kutusu.get().strip()   # giris_kutusu.get(): Kullanıcının yazdığı IP'yi alır
    if not ip:                        # Eğer IP boşsa
        sonuc_etiketi.config(text=" Lütfen bir IP adresi giriniz!", fg="orange")  # Uyarı mesajı
        return
    
    ip = ip_normalizasyon(ip)         # Önceki fonksiyonu çağırarak IP'deki gereksiz sıfırları temizler.
# try / except ValueError ile ipaddress kütüphanesi kullanarak IP'yi doğrulamaya çalışır. Eğer yazılan metin hatalıysa (IP değilse), kırmızı renkli hata mesajı verir.

    try: 
        ip_obj = ipaddress.ip_address(ip)   
    except ValueError:                      
        sonuc_etiketi.config(text=" Bu IP adresi değil!", fg="red")  # Geçersiz IP mesajı
        return
    
    parametre = "-n" if platform.system().lower() == "windows" else "-c"   #platform kütüphanesini kullanarak işletim sistemine göre Ping parametresini belirler (Windows için -n, Mac/Linux için -c).   
    komut = ["ping", parametre, "1", ip]   # ping komutunu hazırlar
    
    try:
        cikti = subprocess.run(komut, stdout=subprocess.PIPE, stderr=subprocess.PIPE)  # ping çalıştırılır
        if cikti.returncode == 0:   # returncode == 0 → ping başarılı
            sonuc_etiketi.config(text=f"{ip} aktif ve erişilebilir ", fg="green")   # IP aktif mesajı
        else:
            sonuc_etiketi.config(text=f"{ip} geçerli ama erişilemez ", fg="orange")  # IP geçerli ama erişilemez
    except Exception as e:   # Sistemde oluşabilecek beklenmedik diğer hataları yakalar ve kırmızı renkle ekrana basar
        sonuc_etiketi.config(text=f"Hata: {e}", fg="red")   # Hata mesajı

# GUI (Grafik Arayüz) kısmı
pencere = tk.Tk()   # Tk(): Ana pencereyi oluşturur
pencere.title("IP Kontrol")   # Pencere başlığı
pencere.geometry("400x200")         # Pencere boyutu
pencere.configure(bg="#232323")   # pencere arka planını siyah yapar

etiket = tk.Label(pencere, text="IP Adresi Giriniz:", font=("Arial", 12),fg="white",bg="#232323")   # Kullanıcıya IP girmesi için yazı düzenleme
etiket.pack(pady=12) #yazım boyutu

giris_kutusu = tk.Entry(pencere, width=30, font=("Arial", 12),fg="white",bg="#232323",bd=2)   # Kullanıcının IP yazacağı kutu düzenleme
giris_kutusu.pack(pady=8) #yazım boyutu

giris_kutusu.bind("<Return>", ip_kontrol)   # Enter tuşuna basıldığında ip_kontrol fonksiyonu çalışır

buton = tk.Button(pencere, text="Kontrol Et", command=ip_kontrol, font=("Arial", 12),fg="white", bg="green")   # Kontrol Et butonu düzenleme
buton.pack(pady=24)  #yazım boyutu

sonuc_etiketi = tk.Label(pencere, text="", font=("Arial", 12),bg="#232323")   # Sonuçların gösterileceği etiket düzenleme
sonuc_etiketi.pack(pady=10) #yazım boyutu

pencere.mainloop()   # mainloop(): Arayüzü çalıştırır ve kullanıcı etkileşimini bekler


