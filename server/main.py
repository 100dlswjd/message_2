from signal import signal
import sys
import socket

from PySide6.QtCore import Slot, QObject, Signal, QEvent
from PySide6.QtWidgets import QMainWindow, QApplication, QListWidgetItem, QWidget
from PySide6.QtNetwork import QTcpServer, QTcpSocket
from PySide6.QtGui import Qt, QKeyEvent

from server_form import Ui_mainWindow

def pressed(widget : QWidget):
    class Filter(QObject):
        pressed = Signal(QKeyEvent)
        def eventFilter(self, watched: QObject, event: QEvent) -> bool:
            if watched == widget and event.type() == QKeyEvent.KeyPress:
                self.pressed.emit(QKeyEvent(event))                
            return super().eventFilter(watched, event)
    filter = Filter(widget)
    widget.installEventFilter(filter)
    return filter.pressed

class Mainwindow(QMainWindow, Ui_mainWindow):
    def __init__(self):
        super(Mainwindow, self).__init__()
        self.setupUi(self)
        self._client_list = list()
        self._item = QListWidgetItem()

        self._server = QTcpServer()
        self._server.listen(port = 9500)
        self._server.newConnection.connect(self.newConnection_handler)
                
        self.btn_message.clicked.connect(self.button_handler)
        self.server_ip = socket.gethostbyname(socket.gethostname())

        pressed(self.lineEdit_message).connect(self.pressed_handler)
        self.label.setText(f"서버 주소 : {self.server_ip}")

    @Slot(QKeyEvent)
    def pressed_handler(self, Key_Event : QKeyEvent):
        if Key_Event.key() == Qt.Key_Return:
            self.btn_message.click()

    @Slot()
    def button_handler(self):
        text = "운영자 : "
        text += self.lineEdit_message.text()
        for client in self._client_list:
            client.write(text.encode())
        item = QListWidgetItem()
        item.setText(text)
        item.setTextAlignment(Qt.AlignRight)
        self.listWidget.addItem(item)
        self.listWidget.scrollToBottom()
        self.lineEdit_message.clear()

    @Slot()
    def newConnection_handler(self):
        self._client_list.append(self._server.nextPendingConnection())
        add_message = "새로운 사용자가 연결 하였습니다. !"
        item = QListWidgetItem()
        item.setText(add_message)
        item.setTextAlignment(Qt.AlignCenter)
        self.listWidget.addItem(item)
        self.listWidget.scrollToBottom()

        for client in self._client_list:
            client.readyRead.connect(self.client_readyRead_handler)
            self.disconnect_client = client.disconnected.connect(self.disconnected_handler)
            
        
    @Slot()
    def client_readyRead_handler(self):
        for client in self._client_list:
            flag = True
            if client.bytesAvailable():
                data = bytes(client.readAll())
                data_decode = data.decode()
                self._item.setTextAlignment(Qt.AlignLeft)
                self.listWidget.addItem(data_decode)
                self.listWidget.scrollToBottom()
                flag = False

            if flag:
                client.write(data_decode.encode())

    @Slot()
    def disconnected_handler(self):
        add_message = "한명의 사용자가 떠났습니다... 흙흙"
        item = QListWidgetItem()
        item.setText(add_message)
        item.setTextAlignment(Qt.AlignCenter)
        self.listWidget.addItem(item)
        self.listWidget.scrollToBottom()
        print(self._client_list)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Mainwindow()
    window.show()
    app.exec()