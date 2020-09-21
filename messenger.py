from datetime import datetime

import requests
from PyQt5 import QtWidgets, QtCore

from clientui import Ui_MainWindow


class Messenger(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, url):
        super().__init__()
        self.setupUi(self)

        self.url = url
        self.after_timestamp = 0
        self.pushButton.pressed.connect(self.button_pressed)
        self.preload()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_messages)
        self.timer.start(1000)

    def button_pressed(self):
        response=None
        name = self.lineEdit.text()
        text = self.textEdit.toPlainText()
        data = {'name': name, 'text': text}
        try:
            response=requests.post(self.url + '/send', json=data) #делает запрос типа пост на функцию сенд сервера, отправляя джейсон типа {'name': name, 'text': text}
        except:
            pass
        if response and response.status_code==200:
            self.textEdit.clear()
            self.textEdit.repaint()
        else:
            self.textBrowser.append('Ваше сообщение не отправлено. сервер не отвечает')


    def update_messages(self):
        response = None
        try:
            response = requests.get(self.url + '/messenger',
                    params={'after_timestamp': self.after_timestamp}) # делает запрос типа гет на функцию messenger сервера с параметром {'after_timestamp': self.timestamp}
        except:
            pass
        if response and response.status_code == 200:
            messages = response.json()['messages']   #если ответ успешно получен, берем из него джейсон по ключу ['messages']
            for i in messages:
                self.edit_mess(i)
                self.after_timestamp = i['timestamp']
            return messages

    def edit_mess(self, message):
        dt = datetime.fromtimestamp(message['timestamp'])
        dt = dt.strftime('%Y/%m%d %H:%M:%S')
        first_line = dt + '  ' + message['name']
        self.textBrowser.append(first_line)
        self.textBrowser.append(message['text'])
        self.textBrowser.append('')
        self.textBrowser.repaint()

    def preload(self):
        while self.update_messages():
            pass

app = QtWidgets.QApplication([])
window = Messenger('http://127.0.0.1:5000')
window.show()
app.exec_()
