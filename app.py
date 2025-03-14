import warnings
from PIL import Image, ImageEnhance
warnings.filterwarnings('ignore')
import tensorflow as tf
from keras.models import load_model
from keras.applications.vgg16 import preprocess_input
import numpy as np
from keras.preprocessing import image
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QLabel, QTabWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from win32com.client import Dispatch
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = ['0']
def speak(str1):
    speak = Dispatch("SAPI.SpVoice")
    speak.Speak(str1)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 650)
        MainWindow.setWindowIcon(QIcon("picture.jpg"))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        # Tạo Tab Widget
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 780, 600))
        # Tab 1:Chẩn đoán
        self.tab1 = QtWidgets.QWidget()
        self.tabWidget.addTab(self.tab1, "Chẩn đoán")
        self.bg_label = QLabel(self.tab1)
    #bố cục của tab 1:
        self.bg_label.setGeometry(QtCore.QRect(0, 0, 780, 600))
        self.bg_label.setPixmap(QtGui.QPixmap("nen1.jpg"))
        self.bg_label.setScaledContents(True)
        self.label_2 = QLabel(self.tab1)
        self.label_2.setGeometry(QtCore.QRect(120, 430, 591, 41)) # vị trí của tiêu đề
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        #Nút tải hình ảnh trong tab 1:
        self.pushButton = QtWidgets.QPushButton(self.tab1)
        self.pushButton.setGeometry(QtCore.QRect(100, 530, 201, 31)) # vị trí của nút bấm' tải hình ảnh'
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("background-color:#DF582C; border-radius: 10px;")
        self.pushButton.setObjectName("pushButton")
        #nút dự đoán trong tab 1:
        self.pushButton_2 = QtWidgets.QPushButton(self.tab1)
        self.pushButton_2.setGeometry(QtCore.QRect(450, 530, 201, 31)) #vị trí của nút bấm ' dự đoán '
        font.setPointSize(12)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("background-color:#DF582C; border-radius: 10px;")
        self.pushButton_2.setObjectName("pushButton_2")

    # Tab 2: Hiển thị ảnh + kết quả
        self.tab2 = QtWidgets.QWidget()
        self.tabWidget.addTab(self.tab2, "Hình ảnh")
        self.image_label = QLabel(self.tab2)
        self.image_label.setGeometry(QtCore.QRect(50, 50, 680, 480)) # vị trí của tab hình ảnh 
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("border: 2px solid black;")
        #Hiển thị kết quả của tab 2
        self.result_label = QLabel(self.tab2)
        self.result_label.setGeometry(QtCore.QRect(50, 530, 680, 40)) # vị trí của kết quả dự đoán của tab hình ảnh
        self.result_label.setAlignment(Qt.AlignCenter)
        font.setPointSize(20)
        font.setBold(True)
        self.result_label.setFont(font)
        self.result_label.setStyleSheet("color: red;")

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Kết hợp các tab
        self.pushButton.clicked.connect(self.upload_image)
        self.pushButton_2.clicked.connect(self.predict_result)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Xử lý ảnh y học"))
        self.label_2.setText(_translate("MainWindow", "Nhận biết bệnh viêm phổi"))
        self.pushButton.setText(_translate("MainWindow", "Upload hình ảnh"))
        self.pushButton_2.setText(_translate("MainWindow", "Dự đoán"))
        self.result_label.setText(_translate("MainWindow", "Kết quả sẽ hiển thị ở đây"))

    def upload_image(self):
        filename, _ = QFileDialog.getOpenFileName()
        if filename:
            self.image_path = filename
            pixmap = QtGui.QPixmap(self.image_path)
            self.image_label.setPixmap(pixmap)
            self.image_label.setScaledContents(True)

    def predict_result(self):
        if hasattr(self, 'image_path'):
            model = load_model('xray.h5')
            img_file = image.load_img(self.image_path, target_size=(224, 224))
            x = image.img_to_array(img_file)
            x = np.expand_dims(x, axis=0)
            img_data = preprocess_input(x)
            result = model.predict(img_data)

            if result[0][0] > 0.5:
                diagnosis = "Bình thường"
                speak("Normal")
            else:
                diagnosis = "Viêm phổi"
                speak("PNEUMONIA")

            self.result_label.setText(f"Kết quả: {diagnosis}")
            self.tabWidget.setCurrentIndex(1)  # Chuyển sang tab hình ảnh sau khi dự đoán
        else:
            print("Chưa có hình ảnh nào được tải lên!")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())