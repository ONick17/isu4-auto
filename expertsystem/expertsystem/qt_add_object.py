# Form implementation generated from reading ui file 'qt_main_db.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
'''
Интерфейс диалога для внесения купленных объектов
'''
from PyQt6 import QtCore, QtWidgets



# Класс диалогового окна
class DialogAddObject(object):
    def __init__(self, mode):
        self.dialog = None
        self.return_ = None
        self.mode = mode


    def setupUi(self, Dialog):
        self.dialog = Dialog
        Dialog.setObjectName("Dialog")



        self.add_functions()
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Ввод купленного объекта"))


    def add_functions(self):
        self.btn_cancel.clicked.connect(self.dialog.done)
        self.btn_accept.clicked.connect(self.accept_)

    def accept_(self):
        self.dialog.accept()