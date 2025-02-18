import os
import sys

import requests
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton

SCREEN_SIZE = [600, 450]
a, b = 20, 20

class Example(QWidget):
    def __init__(self):
        global a, b
        super().__init__()
        self.getImage(a, b)
        self.initUI()

    def getImage(self, a, b):
        print(1)
        server_address = 'https://static-maps.yandex.ru/v1?'
        api_key = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
        ll = 'll=136.068544%2C-23.866516&spn='
        map_request = f"{server_address}{ll}{a},{b}&apikey={api_key}"
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

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
        self.PgDown = QPushButton(self)
        self.PgDown.move(500, 400)
        self.PgDown.setText("Уменьшение")
        self.PgDown.clicked.connect(self.run1)
        self.PgUp = QPushButton(self)
        self.PgUp.move(400, 400)
        self.PgUp.setText("Увеличение")
        self.PgUp.clicked.connect(self.run2)
        self.image.setPixmap(self.pixmap)

    def closeEvent(self, event):
        os.remove(self.map_file)

    def run1(self):
        global a, b
        a /= 2
        b /= 2
        self.update_map()

    def run2(self):
        global a, b
        a *= 2
        b *= 2
        self.update_map()

    def update_map(self):
        server_address = 'https://static-maps.yandex.ru/v1?'
        api_key = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
        ll = 'll=136.068544%2C-23.866516&spn='
        map_request = f"{server_address}{ll}{a},{b}&apikey={api_key}"
        response = requests.get(map_request)
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)
        self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())