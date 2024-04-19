from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu, QPushButton, QFileDialog, QVBoxLayout
import os
import function as tf

Form, Window = uic.loadUiType("architecture/project.ui")

app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()


all_items = []


def getFilesInDirectory(directory):
    # Получаем список файлов в директории
    files = os.listdir(directory)
    
     # Отфильтровываем файлы с расширением .txt и возвращаем их имена без расширения
    txt_files = []
    for file in files:
        # Проверяем, является ли текущий файл файлом (а не директорией) и имеет ли он расширение .txt
        if os.path.isfile(os.path.join(directory, file)) and file.endswith('.txt'):
            # Используем splitext, чтобы разделить имя файла и его расширение
            file_name_without_extension = os.path.splitext(file)[0]
            txt_files.append(file_name_without_extension)
    
    return txt_files



# Функция, которая вызывается при запуске программы
def formLoad():
    # Получаем список файлов в указанной директории
    mames_songs = getFilesInDirectory('database')

    # Добавляем песни, которые есть в директории database
    form.listWidget.clear()
    for name_song in mames_songs:
        form.listWidget.addItem(name_song)

    # Добавление имеющихся песен из listWidget для поиска среди них
    for index in range(form.listWidget.count()):
        item = form.listWidget.item(index)
        all_items.append(item.text())
formLoad()



# Функция поиска среди списка песен
def search():
    found_items = []
    text = form.lineEdit.text()
    found_items.clear()

    for item_text in all_items:
        if text in itemText:
            found_items.append(item_text)

    form.listWidget.clear()

    for itemText in found_items:
        form.listWidget.addItem(itemText)

form.lineEdit.textChanged.connect(search)



# Вывод в файлик по 3 строчечки
# def take_onClick():
#     file_name = 'frontend/output.txt'
#     with open(file_name, 'w') as file:
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
    whole_song = ''
    name_song = ''
    batch = []
    mas_metrics = []
    lines = form.textEdit.toPlainText().split('\n')
    
    # Циклом собираем по 3 строки
    for line in lines:
        if line.strip():
            batch.append(line)
            if name_song == '':
                name_song = line
                batch = []
        if len(batch) == 3:
            metric = round(tf.predict(batch), 5)
            mas_metrics.append(metric)
            whole_song += str(metric) + '\n' + '\n'.join(batch) + '\n\n'
            batch = []
        # Если осталась еще одна строка, то дозаписываем её
    if batch:  
        metric = round(tf.predict(batch), 5)
        mas_metrics.append(metric)
        whole_song += str(metric) + '\n' + '\n'.join(batch) + '\n'

    # Расчёт суммы метрик
    sum_metrics = 0
    for metriс in mas_metrics:
        sum_metrics += metriс

    # Если пользователь ничего не ввёл, то обрабатываем выход из программы
    if len(mas_metrics) == 0:
        return

    # Расчёт среденей метрики
    sr_metric = round(sum_metrics / len(mas_metrics), 5)

    # Запись в файл песни с метриками
    file_name = 'database/' + name_song + '.txt'
    with open(file_name, 'w', encoding='utf8') as file:
        file.write(str(sr_metric) + '\n' + name_song + '\n\n' + whole_song)

    # Добавление в listWidget новой песни
    form.listWidget.addItem(name_song)

    all_items.clear()
    for index in range(form.listWidget.count()):
        item = form.listWidget.item(index)
        all_items.append(item.text())

    # Вывод результатов в label
    if sr_metric < 0.5:
        form.label.setText("Метрика: " + str(sr_metric) + "\nЕсть деструктив")
    else:
         form.label.setText("Метрика: " + str(sr_metric) + "\nНет деструктива")
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



# Функция выгрузки текста из файла в textEdit при нажатии на элемент listWidget
def chooseItem():
    name_song = form.listWidget.currentItem().text()
    file_name = "database/" + str(name_song) + ".txt"
    with open(file_name, 'r', encoding='utf-8') as file:
        metric = file.readline()
        text = file.read()
        
    form.textEdit.setPlainText(text) 
    
    if float(metric) < 0.5:
        form.label.setText("Метрика: " + metric + "Есть деструктив")
    else:
        form.label.setText("Метрика: " + metric + "Нет деструктива")
form.listWidget.clicked.connect(chooseItem)


app.exec()