# Form implementation generated from reading ui file 'qt_dialog_add_object.ui'
#
# Created by: PyQt6 UI code generator 6.6.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(280, 140)
        self.lbl_price = QtWidgets.QLabel(parent=Dialog)
        self.lbl_price.setGeometry(QtCore.QRect(20, 55, 100, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lbl_price.setFont(font)
        self.lbl_price.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.lbl_price.setObjectName("lbl_price")
        self.lbl_object = QtWidgets.QLabel(parent=Dialog)
        self.lbl_object.setGeometry(QtCore.QRect(20, 20, 100, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lbl_object.setFont(font)
        self.lbl_object.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.lbl_object.setObjectName("lbl_object")
        self.btn_accept = QtWidgets.QPushButton(parent=Dialog)
        self.btn_accept.setGeometry(QtCore.QRect(20, 90, 110, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btn_accept.setFont(font)
        self.btn_accept.setObjectName("btn_accept")
        self.btn_cancel = QtWidgets.QPushButton(parent=Dialog)
        self.btn_cancel.setGeometry(QtCore.QRect(150, 90, 110, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btn_cancel.setFont(font)
        self.btn_cancel.setObjectName("btn_cancel")
        self.spnbox_price = QtWidgets.QSpinBox(parent=Dialog)
        self.spnbox_price.setGeometry(QtCore.QRect(130, 55, 50, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.spnbox_price.setFont(font)
        self.spnbox_price.setObjectName("spnbox_price")
        self.cmbox_object = QtWidgets.QComboBox(parent=Dialog)
        self.cmbox_object.setGeometry(QtCore.QRect(130, 20, 130, 22))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.cmbox_object.setFont(font)
        self.cmbox_object.setObjectName("cmbox_object")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.lbl_price.setText(_translate("Dialog", "Цена"))
        self.lbl_object.setText(_translate("Dialog", "Тип объекта"))
        self.btn_accept.setText(_translate("Dialog", "Добавить"))
        self.btn_cancel.setText(_translate("Dialog", "Отмена"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec())
