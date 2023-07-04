import json
from bs4 import BeautifulSoup
import requests
import pandas
class Sinif:
    kitapİsimleri=[]
    Kurİsimleri=[]
    def __init__(self,url) -> None:
        self.url="https://www.kitapyurdu.com/kategori/kitap/1.html"
        self.html=requests.get(self.url).content
        self.soup=BeautifulSoup(self.html,"html.parser")
        Sinif.Kurİsmi(self)
 


    def Kurİsmi(self):
        Bul=self.soup.select("li.mg-b-10>div>div:nth-child(4)")#burada yaptığım şey selenium css selecter ile kullanabilir
        # print(Bul)
        for a in Bul:
            a=a.text
            Sinif.kitapİsimleri.append(a)
            print(a)
            

    
    # def Fiyatlar(self):
    #     Bul=self.soup.select("div.item>a>span:nth-child(2)")
    #     for a in Bul:
    #         a=a.text
    #         Sinif.KurFiyatlar.append(a)
            
    
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