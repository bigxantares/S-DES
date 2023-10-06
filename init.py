import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QIcon, QFont, QPalette, QColor
from SDES import Cipher, PlainTextTransfer, CipherTextTransfer,  Bdecrypt, Adecrypt, Transfers
from GenerateKeys import generate_keys

# SDES_GUI类是用于交互的界面，使用PYQT5进行布局
class SDES_GUI(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置窗口标题和大小
        self.setWindowTitle('S-DES加密解密')
        self.setFixedSize(800, 600)

        # 设置窗口图标
        self.setWindowIcon(QIcon('icon.png'))

        # 设置窗口样式
        self.setStyleSheet("QMainWindow { border: 2px solid red; }")

        # 设置背景颜色
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(180, 180, 180))
        self.setPalette(palette)

        # 创建标签和文本框
        self.plain_label = QLabel('在此处输入明文/密文：')
        self.plain_label.setFont(QFont('微软雅黑', 30))
        self.plain_edit = QLineEdit()
        self.plain_edit.setFont(QFont('微软雅黑', 12))
        self.plain_edit.setStyleSheet("background-color: white;")

        self.key_label = QLabel('在此处输入密钥：')
        self.key_label.setFont(QFont('微软雅黑', 30))
        self.key_edit = QLineEdit()
        self.key_edit.setFont(QFont('微软雅黑', 12))
        self.key_edit.setStyleSheet("background-color: white;")

        self.result_label = QLabel('加密/解密结果：')
        self.result_label.setFont(QFont('微软雅黑', 30))
        self.result_edit = QLineEdit()
        self.result_edit.setFont(QFont('微软雅黑', 12))
        self.result_edit.setStyleSheet("background-color: white;")

        # 创建按钮
        self.encrypt_button = QPushButton('加密(二进制)')
        self.encrypt_button.setFont(QFont('微软雅黑', 20))
        self.encrypt_button.setStyleSheet("background-color: #4C11CC; color: white;")

        self.decrypt_button = QPushButton('解密(二进制)')
        self.decrypt_button.setFont(QFont('微软雅黑', 20))
        self.decrypt_button.setStyleSheet("background-color: #f44336; color: white;")

        self.encrypt_button2 = QPushButton('加密(ASCII码)')
        self.encrypt_button2.setFont(QFont('微软雅黑', 20))
        self.encrypt_button2.setStyleSheet("background-color: #1C9B64; color: white;")

        self.decrypt_button2 = QPushButton('解密(ASCII码)')
        self.decrypt_button2.setFont(QFont('微软雅黑', 20))
        self.decrypt_button2.setStyleSheet("background-color: #AF9546; color: white;")

        self.transferom_button = QPushButton('转换ASCII')
        self.transferom_button.setFont(QFont('微软雅黑', 20))
        self.transferom_button.setStyleSheet("background-color: #2196F3; color: white;")

        self.transferom16_button = QPushButton('转换十六进制')
        self.transferom16_button.setFont(QFont('微软雅黑', 20))
        self.transferom16_button.setStyleSheet("background-color: #812299; color: white;")

        # 创建布局
        vbox1 = QVBoxLayout()
        vbox1.addWidget(self.plain_label)
        vbox1.addWidget(self.plain_edit)
        vbox1.addWidget(self.key_label)
        vbox1.addWidget(self.key_edit)
        vbox1.addWidget(self.result_label)
        vbox1.addWidget(self.result_edit)

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.encrypt_button)
        hbox1.addWidget(self.decrypt_button)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.encrypt_button2)
        hbox2.addWidget(self.decrypt_button2)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.transferom_button)
        hbox3.addWidget(self.transferom16_button)

        vbox2 = QVBoxLayout()
        vbox2.addLayout(vbox1)
        vbox2.addLayout(hbox1)
        vbox2.addLayout(hbox2)
        vbox2.addLayout(hbox3)

        self.setLayout(vbox2)

        # 绑定按钮事件
        self.encrypt_button.clicked.connect(self.encrypt)
        self.decrypt_button.clicked.connect(self.decrypt)
        self.encrypt_button2.clicked.connect(self.encrypt2)
        self.decrypt_button2.clicked.connect(self.decrypt2)
        self.transferom_button.clicked.connect(self.transferom)
        self.transferom16_button.clicked.connect(self.transferom16)

    def transferom(self):
        binary_text = self.result_edit.text()
        # 判断输入的文本是否为二进制
        if not all(c in "01" for c in binary_text):
            QMessageBox.warning(self, "警告", "请使用二进制进行转换")
            return

        ascii_text = ""
        for i in range(0, len(binary_text), 8):
            ascii_text += chr(int(binary_text[i:i + 8], 2))

        # 将转换后的结果设置回文本框中
        self.result_edit.setText(ascii_text)

    def transferom16(self):
        binary_text = self.result_edit.text()
        # 判断输入的文本是否为二进制
        if not all(c in "01" for c in binary_text):
            QMessageBox.warning(self, "警告", "请使用二进制进行转换")
            return

        # 将二进制转换为 十六进制码
        ascii_text = ""
        for i in range(0, len(binary_text), 8):
            ascii_text += "{:02X}".format(int(binary_text[i:i + 8], 2))

        # 将转换后的结果设置回文本框中
        self.result_edit.setText(ascii_text)

    def encrypt(self):
        plaintext = self.plain_edit.text()
        # 判断输入的文本是否为二进制
        if not all(c in "01" for c in plaintext):
            QMessageBox.warning(self, "警告", "请使用二进制进行加密")
            return
        key = self.key_edit.text()

        # 将明文转换为二进制字符串
        plaintext = PlainTextTransfer(plaintext, 'Binary')

        # 生成子密钥
        key1, key2 = generate_keys(key)

        # 加密
        cipher = Cipher(plaintext, [key1, key2])
        ciphertext = cipher.transfer()
        self.result_edit.setText(ciphertext)

    def decrypt(self):
        ciphertext = self.plain_edit.text()
        if not all(c in "01" for c in ciphertext):
            QMessageBox.warning(self, "警告", "请使用二进制进行解密")
            return
        key = self.key_edit.text()
        plaintext =  Bdecrypt(ciphertext, key)
        # 显示结果
        self.result_edit.setText(plaintext)

    def encrypt2(self):
        plaintext = self.plain_edit.text()
        key = self.key_edit.text()

        # 将明文转换为二进制字符串
        plaintext = PlainTextTransfer(plaintext, 'Binary')

        # 生成子密钥
        key1, key2 = generate_keys(key)

        # 加密
        cipher = Cipher(plaintext, [key1, key2])
        ciphertext = cipher.transfer()
        ciphertext = CipherTextTransfer(ciphertext, 'ASCII')
        # 显示结果
        self.result_edit.setText(ciphertext)

    def decrypt2(self):
        ciphertext = self.plain_edit.text()
        key = self.key_edit.text()
        # ASCII码
        plaintext = Adecrypt(ciphertext, key)
        # 显示结果
        self.result_edit.setText(plaintext)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    sdes_gui = SDES_GUI()
    sdes_gui.show()
    sys.exit(app.exec_())