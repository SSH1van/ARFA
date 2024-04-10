from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu, QPushButton, QFileDialog, QVBoxLayout
import time
import os

Form, Window = uic.loadUiType("frontend/project.ui")

app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()


all_items = []
found_items = []


# Функционал поиска среди списка песен
def search():
    s_text = form.lineEdit.text()
    found_items.clear()

    for item_text in all_items:
        if s_text in item_text:
            found_items.append(item_text)

    form.listWidget.clear()

    for item_text in found_items:
        form.listWidget.addItem(item_text)

form.lineEdit.textChanged.connect(search)

for index in range(form.listWidget.count()):
    item = form.listWidget.item(index)
    all_items.append(item.text())

form.lineEdit.textChanged.connect(search)


# Вывод метрики анализа текста песни
def on_click():
    metrik = 0.94534
    time.sleep(1.5)
    form.label.setText("Метрика: " + str(metrik) + "\nНет деструктива")
form.pushButton.clicked.connect(on_click)

# вывод в файлик по 3 строчечки
def take_onClick():
    filename = 'frontend/output.txt'
    with open(filename, 'w') as file:
        lines = form.textEdit.toPlainText().split('\n')
        batch = []
        for line in lines:
            if line.strip():
                batch.append(line)
            if len(batch) == 3:
                file.write('\n'.join(batch) + '\n\n')
                batch = []

        if batch:  # если осталась еще одна строка
            file.write('\n'.join(batch) + '\n')
form.pushButton.clicked.connect(take_onClick)



# Функция открытия файла для загрузки в textEdit
def OpenFile():
    file_name, _ = QFileDialog.getOpenFileName(window, 'открыть файл', './', 'TXT File (*.txt)')
    if file_name:
        with open(file_name, 'r', encoding='utf8') as file:
            text = file.read()
        form.textEdit.setPlainText(text) 
form.pushButton_4.clicked.connect(OpenFile)


# При изменении textEdit удаляется значение текущей метрики
def change():
    form.label.clear()
form.textEdit.textChanged.connect(change)


# Получение словаря метрик из файла
def read_metric_dict():
    metric_dict = {}
    file_name = "frontend/songs/metriks.txt"
    with open(file_name, 'r', encoding='utf8') as file:
        for line in file:
            key, value = line.strip().split(',')
            metric_dict[key] = value
    
    return metric_dict


# Функция выгрузки текста из файла в textEdit при нажатии на элемент listWidget
def choose_Item():
    name_song = form.listWidget.currentItem().text()
    file_name = "frontend/songs/" + str(name_song) + ".txt"
    with open(file_name, 'r', encoding='utf-8') as file:
        text = file.read()
    form.textEdit.setPlainText(text) 
    
    metric_dict = read_metric_dict()
    metrik = metric_dict[name_song]

    if float(metrik) < 0.5:
        form.label.setText("Метрика: " + metrik + "\nЕсть деструктив")
    else:
        form.label.setText("Метрика: " + metrik + "\nНет деструктива")
form.listWidget.clicked.connect(choose_Item)


app.exec()