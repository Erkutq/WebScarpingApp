import json
import time
from bs4 import BeautifulSoup
import requests
import pandas

import pymongo
from pymongo import MongoClient
class Sinif:
    kitapİsimleri_=[]
    Yazarİsimleri_=[]
    KitapFiyat_=[]
    kitapYayincilari=[]
    Sozluk={}
    

    def __init__(self,url) -> None:
        self.url=url
        self.html=requests.get(self.url).content
        self.soup=BeautifulSoup(self.html,"html.parser")
        Sinif.Dbclear(self)# Veritabanından bulunan verilerin silinmesi
        Sinif.kitapİsim(self)
        Sinif.KitapFiyat(self)
        Sinif.Yayinci(self)
        Sinif.yazarİsim(self)
        Sinif.birlestir(self)
        Sinif.Yazdir(self)
        Sinif.read(self)
        Sinif.VeriKontrol_(self)

    

                



    def kitapİsim(self):
        Bul=self.soup.select("li.mg-b-10>div>div:nth-child(4)")#burada yaptığım şey selenium css selecter ile kullanabilir
        # print(Bul)
        for a in Bul:
            a=a.text
            Sinif.kitapİsimleri_.append(a)
        bul_=len(Bul)
        print(f'Bulunan veri sayısı: {bul_}')
            
            
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
    
    def Yayinci(self):
        Bul = self.soup.select('li.mg-b-10>div>div:nth-child(4)>a')
        for a in Bul:
            Url = a['href']
            kitap_response = requests.get(Url)
            if kitap_response.status_code == 200:
                kitapYayinci = BeautifulSoup(kitap_response.content, 'html.parser').select('.pr_producers__publisher a')
                for kitapYayinci_ in kitapYayinci:
                    yayinci=kitapYayinci_.text
                    Sinif.kitapYayincilari.append(yayinci)
            kitap_response.close()  # Web sayfasını kapatma

          


    def birlestir(self):
        Birlestir = zip(Sinif.kitapİsimleri_, Sinif.Yazarİsimleri_, Sinif.KitapFiyat_,Sinif.kitapYayincilari)
        Birlestir = list(Birlestir)
        Birlestir = dict(zip(range(len(Birlestir)), Birlestir))
        Sinif.Sozluk['Kitap'] = Birlestir


     
    def Yazdir(self):
        with open("Veri.json", "w", encoding="UTF-8") as file:
            json.dump(Sinif.Sozluk,file)

    def read(self):
        with open("Veri.json", "r", encoding="UTF-8") as file:
            data = json.load(file)
        kitaplar = data["Kitap"]
        kitap = [kitap[0].strip() for kitap in kitaplar.values()]
        yazar=[kitap[1].strip() for kitap in kitaplar.values()]
        fiyat=[kitap[2].strip() for kitap in kitaplar.values()]
        kitapYayinci=[kitap[3].strip() for kitap in kitaplar.values()]
        sayi=-1
        for kitap,yazar,fiyat,kitapYayinci in zip(kitap,yazar,fiyat,kitapYayinci):
            client = MongoClient('mongodb://localhost:27017')
            db = client['smartmaple']
            collection = db['kitapyurdu']
            data=[{
                'isim':kitap,
                'yazar':yazar,
                'fiyat':fiyat,
                'Yayin':kitapYayinci
                   }]
            
            collection.insert_many(data)
            
    def veriDosyasiAdet(self):
        with open("Veri.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            kitaplar = data["Kitap"]
            kitap = [kitap[0].strip() for kitap in kitaplar.items()]
            kitap=len(kitap)
            return(kitap)#Veri Json Dosyasında bulunan veriler
        
    def VeriKontrol_(self):
        client = MongoClient("mongodb://localhost:27017")
        db = client["smartmaple"]
        collection = db["kitapyurdu"]

        Json_Dosyaları = open('Veri.json')
        Json_Dosyaları = json.load(Json_Dosyaları)

        results = collection.find()
        for document in Json_Dosyaları :
            if document in results:
                print('Veriler güncel değil ') 
            else:
                print('veriler güncel')  
    
    def Dbclear(self):
        # MongoDB'ye bağlanın
        client = MongoClient('mongodb://localhost:27017/')
        db = client['smartmaple']  # veritabanını seçin
        collection = db['kitapyurdu']  # koleksiyonu seçin

        # Tüm kayıtları silin
        result = collection.delete_many({})

        print("Silinen belge sayısı:", result.deleted_count)



    # yazar=[kitap[1].strip() for kitap in kitaplar.values()]
    # fiyat=[kitap[2].strip() for kitap in kitaplar.values()]
    # sayi=-1

Sinif("https://www.kitapyurdu.com/kategori/kitap/1.html")



# url=requests.get("https://www.doviz.com").content
# soup=BeautifulSoup(url,"html.parser")
# print(soup)


# MongoDB sunucusuna bağlanma
