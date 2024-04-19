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


allItems = []


def getFilesInDirectory(directory):
    # Получаем список файлов в директории
    files = os.listdir(directory)
    
     # Отфильтровываем файлы с расширением .txt и возвращаем их имена без расширения
    txtFiles = []
    for file in files:
        # Проверяем, является ли текущий файл файлом (а не директорией) и имеет ли он расширение .txt
        if os.path.isfile(os.path.join(directory, file)) and file.endswith('.txt'):
            # Используем splitext, чтобы разделить имя файла и его расширение
            fileNameWithoutExtension = os.path.splitext(file)[0]
            txtFiles.append(fileNameWithoutExtension)
    
    return txtFiles



# Функция, которая вызывается при запуске программы
def formLoad():
    # Получаем список файлов в указанной директории
    mamesSongs = getFilesInDirectory('database')

    # Добавляем песни, которые есть в директории database
    form.listWidget.clear()
    for nameSong in mamesSongs:
        form.listWidget.addItem(nameSong)

    # Добавление имеющихся песен из listWidget для поиска среди них
    for index in range(form.listWidget.count()):
        item = form.listWidget.item(index)
        allItems.append(item.text())
formLoad()



# Функция поиска среди списка песен
def search():
    foundItems = []
    text = form.lineEdit.text()
    foundItems.clear()

    for itemText in allItems:
        if text in itemText:
            foundItems.append(itemText)

    form.listWidget.clear()

    for itemText in foundItems:
        form.listWidget.addItem(itemText)

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
    nameSong = ''
    batch = []
    masMetrics = []
    lines = form.textEdit.toPlainText().split('\n')
    
    # Циклом собираем по 3 строки
    for line in lines:
        if line.strip():
            batch.append(line)
            if nameSong == '':
                nameSong = line
                batch = []
        if len(batch) == 3:
            metric = round(tf.predict(batch), 5)
            masMetrics.append(metric)
            wholeSong += str(metric) + '\n' + '\n'.join(batch) + '\n\n'
            batch = []
        # Если осталась еще одна строка, то дозаписываем её
    if batch:  
        metric = round(tf.predict(batch), 5)
        masMetrics.append(metric)
        wholeSong += str(metric) + '\n' + '\n'.join(batch) + '\n'

    # Расчёт суммы метрик
    sumMetrics = 0
    for metriс in masMetrics:
        sumMetrics += metriс

    # Если пользователь ничего не ввёл, то обрабатываем выход из программы
    if len(masMetrics) == 0:
        return

    # Расчёт среденей метрики
    srMetric = round(sumMetrics / len(masMetrics), 5)

    # Запись в файл песни с метриками
    filename = 'database/' + nameSong + '.txt'
    with open(filename, 'w', encoding='utf8') as file:
        file.write(str(srMetric) + '\n' + nameSong + '\n\n' + wholeSong)

    # Добавление в listWidget новой песни
    form.listWidget.addItem(nameSong)

    allItems.clear()
    for index in range(form.listWidget.count()):
        item = form.listWidget.item(index)
        allItems.append(item.text())

    # Вывод результатов в label
    if srMetric < 0.5:
        form.label.setText("Метрика: " + str(srMetric) + "\nЕсть деструктив")
    else:
         form.label.setText("Метрика: " + str(srMetric) + "\nНет деструктива")
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
    nameSong = form.listWidget.currentItem().text()
    fileName = "database/" + str(nameSong) + ".txt"
    with open(fileName, 'r', encoding='utf-8') as file:
        metric = file.readline()
        text = file.read()
        
    form.textEdit.setPlainText(text) 
    
    if float(metric) < 0.5:
        form.label.setText("Метрика: " + metric + "Есть деструктив")
    else:
        form.label.setText("Метрика: " + metric + "Нет деструктива")
form.listWidget.clicked.connect(chooseItem)


app.exec()