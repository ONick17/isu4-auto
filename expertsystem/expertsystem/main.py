'''
Прогноз погоды и энергии => Анализ CSV с учётом погрешности - сделали
Аукцион => Динамичные формирование графиков и рекомендации по закупке - сделали
Расстановка зданий => Построение схемы для эффективной передачи энергии - не делаем
Игра => Предложение заготовленных скриптов, предложения по продаже энергии - не делаем
'''


#pandas для работы с csv
#PyQt6  для интерфейса
#sys для открытия проводника
#qt_main - файл с интерфейсом главного окна
import pandas as pd
from PyQt6 import QtWidgets
from qt_main import MyMainWindow
import sys


#Код, запускающий интерфейс
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    main_window = MyMainWindow()
    main_window.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
