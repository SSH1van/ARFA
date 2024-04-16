from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu, QPushButton, QFileDialog, QVBoxLayout
import time
import os
import function as tf

Form, Window = uic.loadUiType("architecture/project.ui")

app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()


all_items = []
found_items = []


# Функция поиска среди списка песен
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


# Вывод в файлик по 3 строчечки
# def take_onClick():
#     filename = 'frontend/output.txt'
#     with open(filename, 'w') as file:
#         lines = form.textEdit.toPlainText().split('\n')
#         batch = []
#         for line in lines:
#             if line.strip():
#                 batch.append(line)
#             if len(batch) == 3:
#                 file.write('\n'.join(batch) + '\n\n')
#                 batch = []

#         if batch:  # если осталась еще одна строка
#             file.write('\n'.join(batch) + '\n')
# form.pushButton.clicked.connect(take_onClick)



def stratPredict():
    wholeSong = ''
    batch = []
    mas_metrics = []
    lines = form.textEdit.toPlainText().split('\n')
    filename = 'architecture/output.txt'
    
    with open(filename, 'w') as file:
        # Циклом собираем по 3 строки
        for line in lines:
            if line.strip():
                batch.append(line)
            if len(batch) == 3:
                wholeSong += '\n'.join(batch) + '\n\n'
                mas_metrics.append(tf.predict(batch))
                batch = []
            # Если осталась еще одна строка, то дозаписываем её
            if batch:  
                wholeSong += '\n'.join(batch) + '\n'
                mas_metrics.append(tf.predict(batch))
    
    # Расчёт суммы метрик
    sum_metrics = 0
    for metriс in mas_metrics:
        sum_metrics += metriс

    # Если пользователь ничего не ввёл, то обрабатываем выход из программы
    if len(mas_metrics) == 0:
        return

    # Расчёт среденей метрики и её вывод
    sr_metric = sum_metrics / len(mas_metrics)

    if sr_metric < 0.5:
        form.label.setText("Метрика: " + str(round(sr_metric, 5)) + "\nЕсть деструктив")
    else:
         form.label.setText("Метрика: " + str(round(sr_metric, 5)) + "\nНет деструктива")
form.pushButton.clicked.connect(stratPredict)




# Функция открытия файла для загрузки в textEdit
def openFile():
    file_name, _ = QFileDialog.getOpenFileName(window, 'открыть файл', 'architecture/', 'TXT File (*.txt)')
    if file_name:
        with open(file_name, 'r', encoding='utf8') as file:
            text = file.read()
        form.textEdit.setPlainText(text) 
form.pushButton_4.clicked.connect(openFile)


# При изменении textEdit удаляется значение текущей метрики
def change():
    form.label.clear()
form.textEdit.textChanged.connect(change)


# Получение словаря метрик из файла
def read_metric_dict():
    metric_dict = {}
    file_name = "database/metriks.txt"
    with open(file_name, 'r', encoding='utf8') as file:
        for line in file:
            key, value = line.strip().split(',')
            metric_dict[key] = value
    
    return metric_dict


# Функция выгрузки текста из файла в textEdit при нажатии на элемент listWidget
def chooseItem():
    name_song = form.listWidget.currentItem().text()
    file_name = "database/" + str(name_song) + ".txt"
    with open(file_name, 'r', encoding='utf-8') as file:
        text = file.read()
    form.textEdit.setPlainText(text) 
    
    metric_dict = read_metric_dict()
    metrik = metric_dict[name_song]

    if float(metrik) < 0.5:
        form.label.setText("Метрика: " + metrik + "\nЕсть деструктив")
    else:
        form.label.setText("Метрика: " + metrik + "\nНет деструктива")
form.listWidget.clicked.connect(chooseItem)


app.exec()