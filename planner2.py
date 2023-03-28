import sys
from PyQt5 import QtCore, uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QTextEdit, QPushButton, QPlainTextEdit, QListWidget, QSlider,QProgressBar, QCompleter, QLineEdit,QVBoxLayout,QWidget, QStackedWidget,QListView,QCalendarWidget, QTableWidgetItem, QTableWidget
import sqlite3

tasks = []

class UI(QMainWindow):
    
    def __init__(self):
        super(UI,self).__init__()

        #Load ui file
        uic.loadUi("untitled.ui", self)

        self.setWindowTitle("project 3")

        #Widget Definitions
        self.calender = self.findChild(QCalendarWidget,"calendarWidget")
        self.list = self.findChild(QListWidget, "listWidget")
        self.addToDay = self.findChild(QPushButton,"addToDay")
        self.taskLineEdit = self.findChild(QLineEdit, "taskLineEdit")
        self.taskTableWidgetDict = {}
        self.calender.selectionChanged.connect(self.change)

        self.addToDay.clicked.connect(self.addTaskToTable)

        self.show()

    def addTaskToTable(self):
        date = self.calender.selectedDate().toPyDate().strftime("%m-%d")
        task = self.taskLineEdit.text()
        self.taskLineEdit.clear()

        if date not in self.taskTableWidgetDict:
            tableWidget = QTableWidget()
            tableWidget.setColumnCount(1)
            tableWidget.setHorizontalHeaderLabels(["Tasks"])
            self.taskTableWidgetDict[date] = tableWidget
            self.list.addItem(date)
            self.list.setItemWidget(QListWidgetItem(date), tableWidget)

        rowPosition = self.taskTableWidgetDict[date].rowCount()
        self.taskTableWidgetDict[date].insertRow(rowPosition)
        self.taskTableWidgetDict[date].setItem(rowPosition , 0, QTableWidgetItem(task))

        db = sqlite3.connect("data.db")
        cursor = db.cursor()
        cursor.execute("INSERT INTO tasks (date, task, completed) VALUES (?,?,?)", (date, task, 0))
        db.commit()

    def updateTaskList(self, date):
        db = sqlite3.connect("data.db")
        cursor = db.cursor()

        query = "SELECT task, completed FROM tasks WHERE date = ?"
        row = (date,)
        results = cursor.execute(query,row).fetchall()
        for result in results:
            item = QListWidgetItem(str(result[0]))
            item.setFlag(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Unchecked)
            self.tasksListWidget.addItem(item)

    def change(self):
        date = self.calender.selectedDate().toPyDate().strftime("%m-%d")
        print("something changed ", date)

        if date in self.taskTableWidgetDict:
            self.list.setItemWidget(QListWidgetItem(date), self.taskTableWidgetDict[date])

        else:
            self.list.clear()
            self.taskTableWidgetDict.clear()
            self.updateTaskList(date)

# Initialize App
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()
