import sys
from PyQt5 import QtWidgets
from Veritabanicekme import Ui_MainWindow
from PyQt5.QtWidgets import QTableWidgetItem, QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QMessageBox
import pymongo
from PyQt5.QtWidgets import QInputDialog



class KitapEkle(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        print('Kitap Ekleme Sınıfı Çalışıyor...')
        self.setWindowTitle("Kitap Ekle")
        self.layout = QVBoxLayout(self)# Bu kod sıranın dikey bir biçimde

        self.textbox1 = QLineEdit(self)
        self.layout.addWidget(QLabel("Kitap: "))
        self.layout.addWidget(self.textbox1)

        self.textbox2 = QLineEdit(self)
        self.layout.addWidget(QLabel("Yazar: "))
        self.layout.addWidget(self.textbox2)

        self.textbox3 = QLineEdit(self)
        self.layout.addWidget(QLabel("Fiyat: "))
        self.layout.addWidget(self.textbox3)

        self.textbox4 = QLineEdit(self)
        self.layout.addWidget(QLabel("Yayıncı: "))
        self.layout.addWidget(self.textbox4)

        self.button = QtWidgets.QPushButton('Ekle', self)
        self.layout.addWidget(self.button)
        self.button.clicked.connect(self.handle_button_click)

    def handle_button_click(self):
        #Verilerin eklendiği kısım
        textbox1_value = self.textbox1.text()
        textbox2_value = self.textbox2.text()
        textbox3_value = self.textbox3.text()
        textbox4_value = self.textbox4.text()
        self.close()
        Secim=QMessageBox.question(self,f'Kitap Ekle','Bu kitabı eklendiniz \n Kitap: '+textbox1_value+'\n Yazar :'+textbox2_value+'\n Fiyat :'+textbox3_value+'\n'+' Yayıncı :'+textbox4_value,QMessageBox.Yes | QMessageBox.No)
        if Secim==QMessageBox.Yes:
            row_count = self.parent().ui.tableWidget.rowCount()
            self.parent().ui.tableWidget.insertRow(row_count)

            self.parent().ui.tableWidget.setItem(row_count, 0, QTableWidgetItem(textbox1_value))
            self.parent().ui.tableWidget.setItem(row_count, 1, QTableWidgetItem(textbox2_value))
            self.parent().ui.tableWidget.setItem(row_count, 2, QTableWidgetItem(textbox3_value))
            self.parent().ui.tableWidget.setItem(row_count, 3, QTableWidgetItem(textbox4_value))
            for a in KitapEkle.VeritabaninaEkle(self):
                print(a)

            self.close()
        else:
            self.close()

    def VeritabaninaEkle(self):

        client = pymongo.MongoClient('mongodb://localhost:27017/')
        db = client['smartmaple']
        collection = db['kitapsepeti']
        data = {
            'isim': self.textbox1.text(),
            'yazar': self.textbox2.text(),
            'fiyat': self.textbox3.text(),
            'Yayin':self.textbox4.text()
        }
        result = collection.insert_one(data)
        return data.items()


class Guncelleme_Penceresi(QDialog):
    def __init__(self, parent=None):
            super().__init__(parent)
            print('Güncelleme Sınıfı Çalışıyor...')
            for a in myApp.Secim:
                self.setWindowTitle("Güncelleme Sayfası")
                self.layout = QVBoxLayout(self)# Bu kod sıranın dikey bir biçimde

                self.textbox1 = QLineEdit(self)
                self.layout.addWidget(QLabel("Kitap: "))
                self.textbox1.setText(a['KitapAdi'])
                self.layout.addWidget(self.textbox1)

                self.textbox2 = QLineEdit(self)
                self.layout.addWidget(QLabel("Yazar: "))
                self.textbox2.setText(a['KitapYazari'])

                self.layout.addWidget(self.textbox2)

                self.textbox3 = QLineEdit(self)
                self.layout.addWidget(QLabel("Fiyat: "))
                self.textbox3.setText(a['KitapFiyati'])

                self.layout.addWidget(self.textbox3)
                self.textbox4 = QLineEdit(self)
                self.textbox4.setText(a['kitapYayinci'])

                self.layout.addWidget(QLabel("Yayıncı: "))
                self.layout.addWidget(self.textbox4)

                self.button = QtWidgets.QPushButton('Güncelle', self)#gelen pencereye bir button koyduk bu button bizi bastığımız anda ekleme yaptırıyor.Bütün class yapılarının içerisinde bulunması gerekiyor çünkü bütün classlarda bir işlem gerçekleşmeli.
                self.layout.addWidget(self.button)
                self.button.clicked.connect(self.handle_button_click)
                
    #güncelle butonuna basınca çıkan ikinci button
    def handle_button_click(self):
        textbox1_value = self.textbox1.text()
        textbox2_value = self.textbox2.text()
        textbox3_value = self.textbox3.text()
        textbox4_value = self.textbox4.text()

        result = QMessageBox.information(self, 'Güncelleme İşlemi Sayfası', 'Güncelleme işlemi yapılacak. emin misin?', QMessageBox.Yes | QMessageBox.No)
        if result == QMessageBox.Yes:
            client = pymongo.MongoClient('mongodb://localhost:27017/')
            db = client['smartmaple']
            collection = db['kitapsepeti']
            current_row = self.parent().ui.tableWidget.currentRow()

            # Güncellenecek veriler
            my_query = {
                'isim': self.parent().ui.tableWidget.item(current_row, 0).text(),
                'yazar': self.parent().ui.tableWidget.item(current_row, 1).text(),
                'fiyat': self.parent().ui.tableWidget.item(current_row, 2).text(),
                'Yayin': self.parent().ui.tableWidget.item(current_row, 3).text()
            }

            # Yeni veriler
            update = {
                '$set': {
                    'isim': textbox1_value,
                    'yazar': textbox2_value,
                    'fiyat': textbox3_value,
                    'Yayin': textbox4_value
                }
            }

            collection.update_one(my_query, update)  # Doğru parametreleri kullanarak güncelleme işlemini gerçekleştirin

            # Tablodaki verileri güncelle
            self.parent().ui.tableWidget.item(current_row, 0).setText(textbox1_value)
            self.parent().ui.tableWidget.item(current_row, 1).setText(textbox2_value)
            self.parent().ui.tableWidget.item(current_row, 2).setText(textbox3_value)
            self.parent().ui.tableWidget.item(current_row, 3).setText(textbox4_value)

            self.close()
        else:
            self.close()

class Silme_Penceresi(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        print('Silme Sınıfı Çalışıyor...')
        selected_items = self.parent().ui.tableWidget.selectedItems()#Seçtiğim Satır
        result = QMessageBox.question(self, 'Silme Ekranı', 'Bu kaydı silmek istediğinize emin misiniz?', QMessageBox.Yes | QMessageBox.No)
        if result == QMessageBox.Yes:
            self.delete_selected_items(selected_items)
            self.parent().Tablo()# Tablo Güncellemesi yapar

    def delete_selected_items(self, selected_items):
        client = pymongo.MongoClient('mongodb://localhost:27017/')
        db = client['smartmaple']
        collection = db['kitapsepeti']

        for item in selected_items:
            row = item.row()#Seçilen itemin satır numarasını gösteriyor
            isim = self.parent().ui.tableWidget.item(row, 0).text()#birinci satırın 0 ıncı sütünu 
            yazar = self.parent().ui.tableWidget.item(row, 1).text()
            fiyat = self.parent().ui.tableWidget.item(row, 2).text()
            yayinci = self.parent().ui.tableWidget.item(row, 3).text()

            my_query = {
                'isim': isim,
                'yazar': yazar,
                'fiyat': fiyat,
                'Yayin': yayinci
            }
            collection.delete_one(my_query)#seçilen itemi veritabanından siliyor

            self.parent().ui.tableWidget.removeRow(row)#Seçilen itemin satırı siliyor
        

    
   
        # Belgeleri silin            
                  
#İlk açılan pencere
class myApp(QtWidgets.QMainWindow):
    Secim=[]
    def __init__(self):
        print('Program Sınıfı Çalışıyor...'.title())
        super(myApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.Tablo()#Verilerin gösterilmesi
        self.ui.eklebt.clicked.connect(self.ekle)
        self.ui.pushButton.clicked.connect(self.guncelle)
        self.ui.tableWidget.itemClicked.connect(self.secim)
        self.ui.silbtn.clicked.connect(self.delete)
        self.ui.label.setText('Smart Maple| Kitap Sepeti')
        
    def secim(self):#Seçtiğim veriyi bir listeye atıyorum attığım listeden güncellem metoduna verileri çekiyorum
        for item in self.ui.tableWidget.selectedIndexes():
            isim=item.row()
            item=self.ui.tableWidget.item(isim,0)
            item2=self.ui.tableWidget.item(isim,1)
            item3=self.ui.tableWidget.item(isim,2)
            item4=self.ui.tableWidget.item(isim,3)

            liste=({'KitapAdi':item.text(),
                        'KitapYazari':item2.text(),
                        'KitapFiyati':item3.text(),
                        'kitapYayinci':item4.text()
                        })

            myApp.Secim.append(liste)
            if len(myApp.Secim)>=2:
                del myApp.Secim[0]   

            print(f'Kitap İsimi \t{item.text()}\nKitap Yazarı \t{item2.text()}\nKitap Fiyati \t{item3.text()} \nKitap yayıncısı \t{item4.text()}\n------------------------------------------\n')

    def Tablo(self):
        self.ui.tableWidget.setRowCount(1)
        self.ui.tableWidget.setColumnCount(4)
        self.ui.tableWidget.setHorizontalHeaderLabels(('Kitap', 'Yazar', 'Fiyat', 'Yayın'))

        # Establish a connection to MongoDB
        client = pymongo.MongoClient("mongodb://localhost:27017")
        db = client["smartmaple"]
        collection = db["kitapsepeti"]
        data = collection.find()

        self.row_count = collection.count_documents({})  # Get the count of documents in the collection
        self.ui.tableWidget.setRowCount(self.row_count)  # Set the number of rows in the table widget

        row = 0
        for document in data:
            field1 = document["isim"]
            field2 = document["yazar"]
            field3 = document["fiyat"]
            field4 = document["Yayin"]

            self.ui.tableWidget.setItem(row, 0, QTableWidgetItem(field1))
            self.ui.tableWidget.setItem(row, 1, QTableWidgetItem(field2))
            self.ui.tableWidget.setItem(row, 2, QTableWidgetItem(field3))
            self.ui.tableWidget.setItem(row, 3, QTableWidgetItem(field4))

            row += 1

        client.close()

    def ekle(self):
        dialog = KitapEkle(self)
        if dialog.exec_() == QDialog.Accepted:#Kullanıcı dialog sınıfını kapattığında diğer sayfayı açar
            textbox1_value = dialog.textbox1.text()#Dialog sınıfında bulunan textbox verisini alıyoruz 
            textbox2_value = dialog.textbox2.text()
            textbox3_value = dialog.textbox3.text()
            textbox4_value = dialog.textbox4.text()
            

            row_count = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(row_count)#Tabloda bulunan veri sayısını alıyoruz.

            self.ui.tableWidget.setItem(row_count, 0, QTableWidgetItem(textbox1_value))#Tabloya verilern eklendiği bölümler.
            self.ui.tableWidget.setItem(row_count, 1, QTableWidgetItem(textbox2_value))
            self.ui.tableWidget.setItem(row_count, 2, QTableWidgetItem(textbox3_value))
            self.ui.tableWidget.setItem(row_count, 3, QTableWidgetItem(textbox4_value))

    def guncelle(self):
        try:
            test=myApp.Secim
            GuncellePenceresi = Guncelleme_Penceresi(self)
            isim=GuncellePenceresi.textbox1.text()
            if GuncellePenceresi.exec_() == QDialog.Accepted:#Kullanıcı dialog sınıfını kapattığında diğer sayfayı açar
                for a in test:
                    print(isim)
        except:AttributeError
        print('lütfen güncelleme yapabilmek için bir değer seçiniz...'.title())

    def delete(self):
        isim=Silme_Penceresi(self)
        # if isim.exec_() == QDialog.Accepted:
        #     print('Açıldı')
            
def app():
    app = QtWidgets.QApplication(sys.argv)
    win = myApp()
    win.show()
    sys.exit(app.exec_())


app()  # Call the app() function to start the application
