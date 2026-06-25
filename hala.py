import os
import stat
import hashlib
import datetime

def baslat():
    try:
        # Kullanıcıdan klasör yolunu istiyoruz
        klasor_yolu = input("Kontrol edilecek klasör yolunu yazın: ")
        bulunan = 0

        # Eğer yol mevcutsa dosyaları tarıyoruz
        if os.path.exists(klasor_yolu):
            for ana_dizin, _, dosya_listesi in os.walk(klasor_yolu):
                for isim in dosya_listesi:
                    tam_yol = os.path.join(ana_dizin, isim)
                    izin = os.stat(tam_yol).st_mode

                    if stat.S_IMODE(izin) == 0o777:
                        print("777 yetkili dosya bulundu:", tam_yol)
                        bulunan += 1

            print("Toplam 777 yetkili dosya:", bulunan)
        else:
            # Yol yoksa sadece uyarı veriyoruz ama devam ediyoruz
            print("⚠️ Bu yol mevcut değil, dosya taraması yapılmadı.")

        # Kullanıcıdan bir anahtar kelime alıyoruz
        anahtar = input("Hash için bir kelime girin: ")

        # SHA256 hash değerini hesaplıyoruz
        sonuc = hashlib.sha256(anahtar.encode()).hexdigest()
        print("SHA256 sonucu:", sonuc)

        # İşlemin bitiş zamanını gösteriyoruz
        print("Tamamlanma zamanı:", datetime.datetime.now())

    except Exception as sorun:
        print("Bir sorun oluştu:", str(sorun))

if __name__== "__main__":
    baslat()