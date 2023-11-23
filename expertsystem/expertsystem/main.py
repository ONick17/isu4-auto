'''
1. Прогноз погоды и энергии => Анализ CSV с учётом погрешности
2. Аукцион => Динамичные формирование графиков и рекомендации по закупке
3. Расстановка зданий => Построение схемы для эффективной передачи энергии
4. Игра => Предложение заготовленных скриптов, предложения по продаже энергии
'''

#этап 0
#pandas для работы с csv
#PyQt6  для интерфейса
#sys для открытия проводника
#qt_main - файл с интерфейсом главного окна
import pandas as pd
from PyQt6 import QtWidgets
from qt_main import MyMainWindow
import sys

#этап 1: считывание csv, накидывание погрешности (15%)

#Код, запускающий интерфейс
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    main_window = MyMainWindow()
    main_window.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
