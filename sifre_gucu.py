import tkinter as tk 
import re
def kontrol_et (event=None):
    sifre=giris.get()
    puan=0
    eksekler=[]
    if len(sifre)>=8 : puan+=1
    else: eksekler.append("en az 8 karekter")
    if any(k.isupper() for k in sifre): puan+=1
    else: eksekler.append('en az 1 buyuk harf')
    if any(k.isdigit()for k in sifre): puan+=1
    else: eksekler.append("en az 1 rakam")
    if re.search(r"[@!#$%*?^&]",sifre): puan+=1
    else: eksekler.append("en az 1 ozel karekter")
    if puan<=1: mesaj,renk="cok zayif","red"
    elif puan==2: mesaj,renk="zayif","orange"
    elif puan==3: mesaj,renk="orta","yellow"
    else: mesaj,renk="guclu","green"

    sonuc.config(text=mesaj,fg=renk)
    if eksekler:
        ipucu.config(text="\n".join(eksekler),fg="grey")
    else:
         ipucu.config(text="her sey tam",fg="grey")
def temizle():
    giris.delete(0,tk.END)
    sonuc.config(text="")
    ipucu.config(text="")
def gizli_goster():
    if giris.cget("show")=="*":
       giris.config(show="")
       gizli_btn.config(text="gizle")
    else:
        giris.config(show="*")
        gizli_btn.config(text="goster")
pencere=tk.Tk()
pencere.title("sifre guc olcer")
pencere.geometry("500x300")
pencere.configure(bg="#1e1e1e")

baslik=tk.Label(pencere,text="sifriniz girin",font=("Arial",13),bg="#1e1e1e",fg="white")
baslik.pack(pady=10)

giris=tk.Entry(pencere,show="*",font=("Arial",9),width=22,bg="white",fg="#1e1e1e")
giris.pack()
giris.bind("<KeyRelease>",kontrol_et)

sonuc=tk.Label(pencere,text="",font=("Arial",10,"bold"),bg="#1e1e1e")
sonuc.pack(pady=5)

ipucu=tk.Label(pencere,text="",bg="#1e1e1e",font=("Arial",11))
ipucu.pack(pady=4)

btn_frame=tk.Frame(pencere,bg="#1e1e1e")
btn_frame.pack(pady=3)

tk.Button(btn_frame,text="temizle",command=temizle,bg="#1e1e1e",fg="white").pack(side=tk.LEFT,padx=6)
gizli_btn=tk.Button(btn_frame,text="goster",command=gizli_goster,bg="#1e1e1e",fg="white")
gizli_btn.pack(side=tk.LEFT,padx=6)

pencere.mainloop()
