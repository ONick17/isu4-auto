'''
Интерфейс главного окна.
Помимо настроек главного окна присутствуют все его функции.
'''

from PyQt6 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
from myparser import parse

#Класс для отображения графиков
class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

#Класс с интерфейсом главного окна
class MyMainWindow(object):
    def __init__(self):
        self.data_to_show = []

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 800)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.btn_start = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btn_start.setGeometry(QtCore.QRect(400, 80, 200, 50))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.btn_start.setFont(font)
        self.btn_start.setStyleSheet("")
        self.btn_start.setObjectName("btn_start")
        self.btn_start.setEnabled(False)
        self.lbl_select_config = QtWidgets.QLabel(parent=self.centralwidget)
        self.lbl_select_config.setGeometry(QtCore.QRect(300, 40, 80, 20))
        self.lbl_select_config.setObjectName("lbl_select_config")
        self.lbl_error = QtWidgets.QLabel(parent=self.centralwidget)
        self.lbl_error.setGeometry(QtCore.QRect(300, 10, 400, 20))
        self.lbl_error.setStyleSheet("color: red;")
        self.lbl_error.setTextFormat(QtCore.Qt.TextFormat.PlainText)
        self.lbl_error.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lbl_error.setObjectName("lbl_error")
        self.lnedit_select_config = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.lnedit_select_config.setGeometry(QtCore.QRect(390, 40, 230, 20))
        self.lnedit_select_config.setObjectName("lnedit_select_config")
        self.btn_select_config = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btn_select_config.setGeometry(QtCore.QRect(620, 40, 70, 20))
        self.btn_select_config.setObjectName("btn_select_config")

        self.pyplot = MplCanvas(self, width=5, height=4, dpi=100)
        # self.pyplot.axes.plot()

        self.toolbar = NavigationToolbar2QT(self.pyplot, parent=self.centralwidget)

        self.pyplot_layout = QtWidgets.QVBoxLayout()
        self.pyplot_layout.addWidget(self.pyplot)
        self.pyplot_layout.addWidget(self.toolbar)
        self.pyplot_widget = QtWidgets.QWidget(parent=self.centralwidget)
        self.pyplot_widget.setLayout(self.pyplot_layout)
        self.pyplot_widget.setGeometry(QtCore.QRect(20, 140, 960, 640))
        self.pyplot_widget.setObjectName("pyplot_area")

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.add_functions()

    #Присвоение элементам интерфейса надписей или дефолтных значений
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Main Window"))
        self.btn_start.setText(_translate("MainWindow", "ЗАПУСК"))
        self.lbl_select_config.setText(_translate("MainWindow", "Путь к файлу:"))
        self.lbl_error.setText(_translate("MainWindow", "Выберите файл с прогнозом (в расширении csv)"))
        self.btn_select_config.setText(_translate("MainWindow", "Указать"))

    #Подключение функций к элементам интерфейса
    def add_functions(self):
        self.btn_select_config.clicked.connect(self.browse_files)
        self.lnedit_select_config.textChanged.connect(self.check_file)
        self.btn_start.clicked.connect(self.stage_start)
        '''
        #Доступ к разным меню настроек
        self.menu_settings_db.triggered.connect(self.settingsDB)
        self.menu_settings_config.triggered.connect(self.settingsConfig)
        '''
    
    #Открытие проводника для выбора файла
    def browse_files(self):
        fl = QtWidgets.QFileDialog.getOpenFileName(None, "Choose forecast", "", "(*.csv)")
        self.lnedit_select_config.setText(fl[0])

    #Автоматическая проверка указанного файла на корректность
    def check_file(self):
        #Пытается считать путь к файлу
        fl = self.lnedit_select_config.text()
        if (fl == "") or (fl.isspace()):
            self.lbl_error.setText("Выберите файл с прогнозом (в расширении csv)")
            self.btn_start.setEnabled(False)
        else:
            #Чтение ожидаемого файла
            try:
                self.data_to_show = parse(fl)
                self.lbl_error.setText("")
                self.btn_start.setEnabled(True)
            except Exception:
                self.lbl_error.setText("С файлом что-то не так!")
                self.data_to_show = []

    def stage_start(self):
        self.pyplot.axes.cla()
        for building in list(self.data_to_show.keys()):
            # plt.legend(list(data.keys()))
            self.pyplot.axes.plot(self.data_to_show[building], label=building)
            self.pyplot.axes.legend()
            self.pyplot.draw()
        
        """
        #Создание и вывод окна с результатами, в которое передаются результаты, общее время тестирования, дата и наименование устройства
        answers_window = QtWidgets.QDialog()
        answers_window.ui = MyAnswersWindow(anss, time_all, date, name, db_settings)
        answers_window.ui.setupUi(answers_window)
        answers_window.exec_()
        #answers_window.show()
        #и exec, и show отображают окно, из-за чего двойное их использование заставляет окно закрываться только со второго раза
        #в чём между ними разница я пока не увидел, так что оставляю только exec
        #upd: видимо show просто показывает контент и сразу же продолжает код, а exec сначала ждёт когда показанный контент закроется
        """
