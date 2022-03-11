import sys

from PySide6.QtCore import Slot, QObject, Signal, QEvent
from PySide6.QtWidgets import QMainWindow, QApplication, QListWidgetItem, QDialog, QWidget
from PySide6.QtNetwork import QTcpSocket
from PySide6.QtGui import Qt, QKeyEvent 

from client_form import Ui_mainWindow
from name_set import Ui_Form

def pressed(widget : QWidget):
    class Filter(QObject):
        pressed = Signal(QKeyEvent)

        def eventFilter(self, watched: QObject, event: QEvent) -> bool:
            if watched == widget and event.type() == QEvent.KeyPress:
                self.pressed.emit(QKeyEvent(event))
            return super().eventFilter(watched, event)

    filter = Filter(widget)
    widget.installEventFilter(filter)

    return filter.pressed

class name_set(QDialog, Ui_Form):
    def __init__(self):
        super(name_set, self).__init__()
        self.setupUi(self)
        self.flag = False
        self.btn_ok.clicked.connect(self.click_handler)
        self.exec()

    def result(self):
        return self.flag, self.lineEdit.text()

    @Slot()
    def click_handler(self):
        self.flag = True
        self.close()
        
class Mainwindow(QMainWindow, Ui_mainWindow):
    def __init__(self):
        super(Mainwindow, self).__init__()
        self.setupUi(self)
        self.bind_flag = False
        self._ip = ""
        self.name = "알수없음"

        self.action_name_set.triggered.connect(self.triggered_handler)

        self._sock = QTcpSocket()
        self._sock.readyRead.connect(self.readyRead_handler)
        self._sock.connected.connect(self.connect_handler)
        self._sock.errorOccurred.connect(self.error_handler)
        self._sock.disconnected.connect(self.disconnect_handler)

        self.btn_ip_set.clicked.connect(self.btn_ip_handler)

        self.btn_message.clicked.connect(self.btn_message_handler)
        pressed(self.lineEdit_message).connect(self.message_press_handler)
        pressed(self.lineEdit_ip_set).connect(self.ip_set_press_handler)

    @Slot(QKeyEvent)
    def ip_set_press_handler(self, Key_Event : QKeyEvent):
        if Key_Event.key() == Qt.Key_Return:
            self.btn_ip_set.click()

    @Slot(QKeyEvent)
    def message_press_handler(self, Key_Event : QKeyEvent):
        if Key_Event.key() == Qt.Key_Return:
            self.btn_message.click()
    
    @Slot()
    def triggered_handler(self):
        flag, name = name_set.result(name_set())
        if flag:
            befor_name = self.name
            if len(name) > 10:
                name = name[:10]
            self.name = name
            opcode = "@"
            opcode += befor_name
            opcode += "_"
            opcode += self.name
            self._sock.write(opcode.encode())

    @Slot()
    def disconnect_handler(self):
        self.label.setText("연결이 해제되었습니다.")
        self.btn_ip_set.click()
        message = "연결이 해제되었습니다. !"
        item = QListWidgetItem()
        item.setText(message)
        item.setTextAlignment(Qt.AlignCenter)
        self.listWidget.addItem(item)
        self.listWidget.scrollToBottom()

    @Slot(QTcpSocket.SocketError)
    def error_handler(self, error_code : QTcpSocket.SocketError):
        if error_code:
            message = "연결중입니다..."
            item = QListWidgetItem()
            item.setText(message)
            item.setTextAlignment(Qt.AlignCenter)
            self.listWidget.addItem(item)
            self.listWidget.scrollToBottom()

    @Slot()
    def connect_handler(self):
        message = "접속 되었습니다."
        item = QListWidgetItem()
        item.setText(message)
        item.setTextAlignment(Qt.AlignCenter)
        self.listWidget.addItem(item)
        self.listWidget.scrollToBottom()
        self.btn_ip_set.setText("연결 끊기")
        self.bind_flag = True

    @Slot()
    def readyRead_handler(self):
        if self._sock.bytesAvailable():
            data = bytes(self._sock.readAll())
            data = data.decode()
            item = QListWidgetItem()
            item.setText(data)
            item.setTextAlignment(Qt.AlignLeft)
            self.listWidget.addItem(item)
            self.listWidget.scrollToBottom()

    @Slot()
    def btn_ip_handler(self):
        if self.bind_flag == False:
            ip_set = "현재 서버 : "
            ip = self.lineEdit_ip_set.text()
            ip_set += ip
            self.label.setText(ip_set)
            self._sock.connectToHost(ip, 9500)        
            self.lineEdit_ip_set.clear()            

        elif self.bind_flag == True:
            self._sock.disconnectFromHost()
            self.label.setText("연결이 해제되었습니다.")
            self.btn_ip_set.setText("접속")
            self.bind_flag = False

    @Slot()
    def btn_message_handler(self):
        message = f"!{self.name} : {self.lineEdit_message.text()}"
        self._sock.write(message.encode())
        item = QListWidgetItem()
        item.setText(message[1:])
        item.setTextAlignment(Qt.AlignRight)
        self.listWidget.addItem(item)
        self.listWidget.scrollToBottom()
        self.lineEdit_message.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Mainwindow()
    window.show()
    app.exec()