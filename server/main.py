import sys
import socket

from qt_material import apply_stylesheet
from PySide6.QtCore import Slot, QObject, Signal, QEvent
from PySide6.QtWidgets import QMainWindow, QApplication, QListWidgetItem, QWidget
from PySide6.QtNetwork import QTcpServer
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
        if len(self.lineEdit_message.text()) > 0:
            text = "운영자 : "
            text += self.lineEdit_message.text()
            item = QListWidgetItem()
            if text[-5:] == "@list":
                message = f"현재 연결 수 : {len(self._client_list)}"
                item.setText(message)
                item.setTextAlignment(Qt.AlignCenter)
                self.listWidget.addItem(item)
                self.listWidget.scrollToBottom()
                self.lineEdit_message.clear()

            elif text[-5:] == "@help":
                text = "@list : 연결된 수 \n@list_info : 닉네임, ip 표시"
                item.setText(text)
                item.setTextAlignment(Qt.AlignCenter)
                self.listWidget.addItem(item)
                self.listWidget.scrollToBottom()
                self.lineEdit_message.clear()

            else:
                item.setText(text)
                item.setTextAlignment(Qt.AlignRight)
                for client in self._client_list:
                    client.write(text.encode())
                self.listWidget.addItem(item)
                self.listWidget.scrollToBottom()
                self.lineEdit_message.clear()

    @Slot()
    def newConnection_handler(self):
        self._client_list.append(self._server.nextPendingConnection())        
        add_message = "새로운 사용자가 연결 하였습니다. !"
        for clients in self._client_list:
            clients.write(add_message.encode())
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
        for read_client in self._client_list:
            if read_client.bytesAvailable():
                # 명령어 코드 읽고 판단해줘야함 !
                data = bytes(read_client.readAll())
                data_decode = data.decode()
                item = QListWidgetItem()

                if data_decode[0] == "@":
                    data_decode = data_decode[1:]
                    data_decode = data_decode.split("_")
                    item.setText(f"{data_decode[0]} -> {data_decode[1]}")
                    item.setTextAlignment(Qt.AlignCenter)
                    self.listWidget.addItem(item)
                    self.listWidget.scrollToBottom()

                elif data_decode[0] == "!":                    
                    data_decode = data_decode[1:]
                    if data_decode[-3:] == "!pc":
                        data_decode = data_decode.split(":")
                        item.setText(f"{data_decode[0]}에서 인원수 조사함 !")
                        item.setTextAlignment(Qt.AlignCenter)
                        self.listWidget.addItem(item)
                        self.listWidget.scrollToBottom()
                        message = f"서버 : {len(self._client_list)}명이 연결되어있습니다."                        
                        read_client.write(message.encode())
                        
                    elif data_decode[-5:] == "!help":
                        message = "!pc : 접속된 사용자의 수\n"
                        read_client.write(message.encode())                        

                    else:
                        item.setText(data_decode)
                        item.setTextAlignment(Qt.AlignLeft)
                        self.listWidget.addItem(item)
                        self.listWidget.scrollToBottom()

                        #message_clinet 는 서버에서 메시지를 보낼 클라이언트임
                        for message_client in self._client_list:
                            if not message_client == read_client:
                                message_client.write(data_decode.encode())
                else:
                    item = QListWidgetItem()
                    item.setText("↖"+data_decode+"↗")
                    item.setTextAlignment(Qt.AlignCenter)
                    self.listWidget.addItem(item)
                    self.listWidget.scrollToBottom()
    
    @Slot()
    def disconnected_handler(self):
        add_message = "한명의 사용자가 떠났습니다... 흙흙"
        item = QListWidgetItem()
        item.setText(add_message)
        item.setTextAlignment(Qt.AlignCenter)
        self.listWidget.addItem(item)
        self.listWidget.scrollToBottom()
        disconnect_client = self.sender()
        self._client_list.remove(disconnect_client)
        for clients in self._client_list:
            clients.write(add_message.encode())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Mainwindow()
    #app.setStyle('Fusion')
    apply_stylesheet(app, theme = 'dark_teal.xml')
    window.show()
    app.exec()