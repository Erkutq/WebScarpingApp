import json
from bs4 import BeautifulSoup
import requests
import pandas

import pymongo
from pymongo import MongoClient
class Sinif:
    kitapİsimleri_=[]
    Yazarİsimleri_=[]
    KitapFiyat_=[]
    Sozluk={}

    def __init__(self,url) -> None:
        self.url=url
        self.html=requests.get(self.url).content
        self.soup=BeautifulSoup(self.html,"html.parser")
        Sinif.kitapİsim(self)
        Sinif.KitapFiyat(self)
        Sinif.yazarİsim(self)
        Sinif.birlestir(self)
        Sinif.Yazdir(self)
        Sinif.read(self)
 


    def kitapİsim(self):
        Bul=self.soup.select("li.mg-b-10>div>div:nth-child(4)")#burada yaptığım şey selenium css selecter ile kullanabilir
        # print(Bul)
        for a in Bul:
            a=a.text
            Sinif.kitapİsimleri_.append(a)
            
            

    def yazarİsim(self):
        Bul=self.soup.select("li.mg-b-10>div>div:nth-child(7)>a")#isimler
        # print(Bul)
        for a in Bul:
            a=a.text
            Sinif.Yazarİsimleri_.append(a)
            

    def KitapFiyat(self):
        Bul=self.soup.select("li.mg-b-10>div>div:nth-child(8)>div:nth-child(2)>span:nth-child(2)")#Kitap Fiyatları
        # print(Bul)
        for a in Bul:
            a=a.text
            Sinif.KitapFiyat_.append(a)
          


    def birlestir(self):
        Birlestir = zip(Sinif.kitapİsimleri_, Sinif.Yazarİsimleri_, Sinif.KitapFiyat_)
        Birlestir = list(Birlestir)
        Birlestir = dict(zip(range(len(Birlestir)), Birlestir))

        Sinif.Sozluk['Kitap'] = Birlestir


        # Sinif.Sozluk['Kitaplar'] = Sinif.KitapFiyat_
     
    def Yazdir(self):
        with open("Veri.json", "w", encoding="utf-8") as file:
            json.dump(Sinif.Sozluk,file)

    def read(self):
        with open("Veri.json", "r", encoding="utf-8") as file:
            data = json.load(file)

# "Kitap" sözlüğündeki fiyatları al
        kitaplar = data["Kitap"]
        kitap = [kitap[0].strip() for kitap in kitaplar.values()]
        yazar=[kitap[1].strip() for kitap in kitaplar.values()]
        fiyat=[kitap[2].strip() for kitap in kitaplar.values()]

        # Fiyatları ekrana yazdır
        for kitap,yazar,fiyat in zip(kitap,yazar,fiyat):
            client = MongoClient('mongodb://localhost:27017')
            db = client['smartmaple']
            collection = db['kitapyurdu']
            data=[{'isim':kitap,
                   'yazar':yazar,
                   'fiyat':fiyat,
                   }]
            collection.insert_many(data)
       

    # def Birlestir(self):
    #     a=zip(Sinif.Kurİsimleri,Sinif.KurFiyatlar)
    #     df=pandas.DataFrame(a,columns=["AD".center(50," "),"Soyad".center(50," ")])
    #     df.drop([0,1], axis=0, inplace=True)#eğer satırdan bir verinin kaldırılmasını istiyorsak bu metodu kullanmamız gerekiyor
    #     # df["İsim"]="MAsa" # Veri eklemek çok basit bu yöntemi kullan
    #     print(df)

    # def Pandas(self):
    #     df=pandas.DataFrame(Sinif.Birlestir,index=[1,2,3,4,5],columns=["AD"])
    #     print(df)

Sinif("https://www.kitapyurdu.com/kategori/kitap/1.html")

# url=requests.get("https://www.doviz.com").content
# soup=BeautifulSoup(url,"html.parser")
# print(soup)


# MongoDB sunucusuna bağlanma
