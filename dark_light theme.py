import os
import sys

import requests
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QCheckBox, QLineEdit, QPushButton

SCREEN_SIZE = [900, 450]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        # 129.732178 62.027221
        # 82.921354%2C55.059254
        # 55.059379, 82.920672
        self.server_address = 'https://static-maps.yandex.ru/v1?'
        # api_key = '7109524c-1ec7-4d24-af0e-9a2fec4e8bca'
        self.api_key = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
        # ll_spn = 'll=37.530887,55.703118&spn=0.002,0.002'
        self.ll_spn = 'll=136.068544%2C-23.866516&spn=20,20'
        self.theme = 'light'
        self.getImage()
        self.initUI()

    def getImage(self):
        # Готовим запрос.

        map_request = f"{self.server_address}{self.ll_spn}&theme={self.theme}&apikey={self.api_key}"
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

        self.checkBox_theme = QCheckBox('dark theme', self)
        self.checkBox_theme.setText("Caption")
        self.checkBox_theme.move(600, 0)
        # self.checkBox_theme.setGeometry(600, 150, 0, 0)
        self.checkBox_theme.resize(90, 20)
        self.checkBox_theme.setText('dark theme')
        self.checkBox_theme.stateChanged.connect(self.theme_changer)

        self.search = QLineEdit(self)
        self.search.move(700, 0)
        self.search.resize(90, 20)

        self.search_but = QPushButton(self)
        self.search_but.move(790, 0)
        self.search_but.resize(50, 20)
        self.search_but.clicked.connect(self.search_obj)

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)

    def theme_changer(self):
        if self.checkBox_theme.isChecked():
            print('dark theme')
            self.theme = 'dark'
            self.getImage()
            self.pixmap = QPixmap(self.map_file)
            self.image.setPixmap(self.pixmap)
            self.image.update()
        else:
            print('light theme')
            self.theme = 'light'
            self.getImage()
            self.pixmap = QPixmap(self.map_file)
            self.image.setPixmap(self.pixmap)
            self.image.update()

    def search_obj(self):
        text_search = self.search.text()
        if text_search:
            server_address = 'http://geocode-maps.yandex.ru/1.x/?'
            api_key = '8013b162-6b42-4997-9691-77b7074026e0'
            # geocode = 'Якутск'
            geocoder_request = f'{server_address}apikey={api_key}&geocode={text_search}&format=json'
            response = requests.get(geocoder_request)
            json_response = response.json()
            if response:
                # Запрос успешно выполнен, печатаем полученные данные.
                print(json_response)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
