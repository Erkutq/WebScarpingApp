import json
import time
from bs4 import BeautifulSoup
import requests
import pandas
import pymongo
from pymongo import MongoClient
import schedule

class Sinif:
    kitapİsimleri_=[]
    Yazarİsimleri_=[]
    KitapFiyat_=[]
    kitapYayincilari=[]
    Sozluk={}

    
    

    def __init__(self,url,BookName,authorname,book_Price,broadcaster,veritabani,jsonDosyası):
        self.url=url
        self.html=requests.get(self.url).content
        self.soup=BeautifulSoup(self.html,"html.parser")
        self.BookName=BookName
        
        self.authorname=authorname
        self.book_Price=book_Price
        self.broadcaster=broadcaster
        self.veritabani=veritabani
        self.jsonDosyası=jsonDosyası
        print('\nBaşlatıldı...')
        
    def run(self):
        Sinif.Dbclear(self)# Veritabanından bulunan verilerin silinmesi
        Sinif.kitapİsim(self)
        Sinif.KitapFiyat(self)
        if(self.broadcaster=='li.mg-b-10>div>div:nth-child(4)>a'):
            Sinif.Yayinci(self)
        else:
            Sinif.yayinci2(self)

        Sinif.yazarİsim(self)
        Sinif.birlestir(self)
        Sinif.Yazdir(self)
        Sinif.read(self)
        # Sinif.VeriKontrol_(self)

    def kitapİsim(self):
        try:
            Bul=self.soup.select(self.BookName)#burada yaptığım şey selenium css selecter ile kullanabilir
            # print(Bul)
            for a in Bul:
                a=a.text.strip()
                Sinif.kitapİsimleri_.append(a)
            print('\nKitap İsimleri Alındı...')
        except:
            print('\nBir sorun meydana geldi path değişmiş olabilir\n'.title())
        # bul_=len(Bul)
        # print(f'Bulunan veri sayısı: {bul_}')
            
            
    def yazarİsim(self):
        try:
            Bul=self.soup.select(self.authorname)#isimler
            # print(Bul)
            for a in Bul:
                a=a.text
                Sinif.Yazarİsimleri_.append(a)
            print('\nYazar İsimleri Alındı...')
        except:
            print('\nBir sorun meydana geldi path değişmiş olabilir\n'.title())

            

    def KitapFiyat(self):
        try:
            Bul=self.soup.select(self.book_Price)#Kitap Fiyatları
            # print(Bul)
            for a in Bul:
                a=a.text.replace('TL',' ').strip()
                Sinif.KitapFiyat_.append(a)
            print('\nKitap Fiyatları Alındı...')
        except:
            print('\nBir sorun meydana geldi path değişmiş olabilir'.title())

        
    def yayinci2(self):
        try:
            Bul=self.soup.select(self.broadcaster)#Kitap Fiyatları
            # print(Bul)
            for a in Bul:
                a=a.text
                Sinif.kitapYayincilari.append(a)
            print('\nKitap Yayıncıları Çekiliyor...')
        except:
            print('\nBir sorun meydana geldi path değişmiş olabilir'.title())


    def Yayinci(self):
        try:
            Bul = self.soup.select("li.mg-b-10>div>div:nth-child(4)>a")
            for a in Bul:
                Url = a['href']
                kitap_response = requests.get(Url)
                if kitap_response.status_code == 200:
                    kitapYayinci = BeautifulSoup(kitap_response.content, 'html.parser').select('.pr_producers__publisher a')
                    for kitapYayinci_ in kitapYayinci:
                        yayinci=kitapYayinci_.text
                        Sinif.kitapYayincilari.append(yayinci)
                kitap_response.close()  # Web sayfasını kapatma
            
            print('\nKitap Yayıncıları Alındı...')
        except:
            print('\nYayinci fonksiyonunda bir Sorun meydana geldi sorun meydana geldi path değişmiş olabilir'.title())


    def birlestir(self):
        try:
            Birlestir = zip(Sinif.kitapİsimleri_, Sinif.Yazarİsimleri_, Sinif.KitapFiyat_,Sinif.kitapYayincilari)
            Birlestir = list(Birlestir)
            Birlestir = dict(zip(range(len(Birlestir)), Birlestir))
            Sinif.Sozluk['Kitap'] = Birlestir
        except:
            print('\nBirleitirme sırasında sorun meydana geldi'.title())
        


     
    def Yazdir(self):
        with open(self.jsonDosyası, "w", encoding="utf-8") as file:
            json.dump(Sinif.Sozluk,file)

    def read(self):
        try:
            with open(self.jsonDosyası, "r", encoding="utf-8") as file:
                data = json.load(file)
            kitaplar = data["Kitap"]
            kitap = [kitap[0].strip() for kitap in kitaplar.values()]
            yazar = [kitap[1].strip() for kitap in kitaplar.values()]
            fiyat = [kitap[2].strip() for kitap in kitaplar.values()]
            kitapYayinci = [kitap[3].strip() for kitap in kitaplar.values()]
            for kitap, yazar, fiyat, kitapYayinci in zip(kitap, yazar, fiyat, kitapYayinci):
                client = MongoClient('mongodb://localhost:27017')
                db = client['smartmaple']
                collection = db[self.veritabani]
                data = [{
                    'isim': kitap,
                    'yazar': yazar,
                    'fiyat': fiyat,
                    'Yayin': kitapYayinci
                }]
                collection.insert_many(data)
            print('\nVeritabanına Veriler Eklendi...')
        except:
            print('\nVeritabanınan eklerken sorun meydana geldi'.title())
            
    def Dbclear(self):
        # MongoDB'ye bağlanın
        client = MongoClient('mongodb://localhost:27017/')
        db = client['smartmaple']  # veritabanını seçin
        collection = db[self.veritabani]  # koleksiyonu seçin

        # Tüm kayıtları silin
        result = collection.delete_many({})

        print("\nSilinen belge sayısı:", result.deleted_count)

def kitapYurdu():
    veritabani='kitapyurdu'
    BookName="li.mg-b-10>div>div:nth-child(4)>a"
    authorname="li.mg-b-10>div>div:nth-child(7)>a"
    book_Price="li.mg-b-10>div>div:nth-child(8)>div:nth-child(2)>span:nth-child(2)"#Kitap Fiyatları
    broadcaster='li.mg-b-10>div>div:nth-child(4)>a'
    jsonDosyası='Veri.json'
    KitapYurdu=Sinif("https://www.kitapyurdu.com/kategori/kitap/1.html",BookName,authorname,book_Price,broadcaster,veritabani,jsonDosyası)
    KitapYurdu.run()

def kitapSepeti():
    veritabani = 'kitapsepeti'
    BookName = "a[class='fl col-12 text-description detailLink']"
    authorname = "a[id='productModelText']"
    book_Price = "div[class='col col-12 currentPrice']"
    broadcaster = "a[class='col col-12 text-title mt']"
    jsonDosyası = 'KitapSepeti.json'
    KitapSepeti = Sinif("https://www.kitapsepeti.com/roman", BookName, authorname, book_Price, broadcaster, veritabani, jsonDosyası)
    KitapSepeti.run()
    
def KoduCalistir():
    islem=input('hangi siteden veri çekmek istediğinizi seçiniz: \n 1.Kitap Yurdu \n 2.Kitap Sepeti \n işlem seçiniz\t'.title()).strip()
    if(islem=='1'):
        print('Kitap Yurdu Çalışıyor...\n')
        print('Biraz zaman alabilir lütfen bekleyiniz...\n'.title())
        kitapYurdu()
    elif (islem=='2'):
        print('\nKitap Sepeti Çalışıyor...')
        kitapSepeti()
        print('\n-BİTTİ...')
    else:
        print('bir değeri seçmediniz'.title())

# seçim yapmak istiyorsak bu şekilde
# schedule.every().day.at('12:00').do(KoduCalistir)



#Buradaki kodlar kodumuzun her gün saat 12 çalışmasını sağlıyacak eğer seçim yapmak istemiyorsak kodu bu şekilde çalıştırırız.
schedule.every().day.at('12:00').do(kitapSepeti)

while True:
    schedule.run_pending()
    time.sleep(1)


