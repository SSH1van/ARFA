from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu, QPushButton, QFileDialog, QVBoxLayout

import app.database.model 
import app.getmetric as gm
import app.database.requests as rq


Form, Window = uic.loadUiType("app/gui/project.ui")
app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()



# Функция, которая вызывается при запуске программы
def formLoad():
    # Получаем список названий песен из БД
    names = rq.get_all_names()

    # Добавляем песни, которые есть в БД
    form.listWidget.clear()
    for name in names:
        form.listWidget.addItem(name)
formLoad()


# Функция поиска среди списка песен
def search():
    names = rq.get_all_names()
    
    found_items = []
    text = form.lineEdit.text().lower()  
    found_items.clear()

    for name in names:
        if text in name.lower(): 
            found_items.append(name)

    form.listWidget.clear()

    for item in found_items:
        form.listWidget.addItem(item)
form.lineEdit.textChanged.connect(search)



def checkingUniqueness(lines):
    names = rq.get_all_names()
    # Проверка по совпадению в названии
    for line in lines:
        if line.strip():
            for name in names:
                if line == name:
                    return True
            break

    # Проверка по наличию уже расставленных метрик
    iteration = 0
    for line in lines:
        try:
            float(line)
            iteration += 1
        except ValueError:
            iteration
    if iteration > 3:
        return True
    return False


def stratPredict():
    text = form.textEdit.toPlainText().strip('\n')
    lines = text.split('\n')

    mas_metrics = []
    parts = []

    text_metrics = ''
    current_part = ''
    name = ''
   
    # Проверяем была ли данный текст уже проанализирован
    if checkingUniqueness(lines): return
    
    # Делим песню по 20 слов и больше
    for line in lines:
        if name == '':
            name = line
        elif line != '':
            current_part += line + '\n'

        length = len(current_part.split())
        if length >= 20:
            parts.append(current_part)
            current_part = ''
    if length < 11 and len(parts) > 0:
        parts[-1] = parts[-1] + current_part
    else:
        parts.append(current_part)

    # Удаляем из текста название песни
    text = text[len(name):].strip()

    # Получаем метрику каждой части по 20 слов
    for song_part in parts:
        metric = round(gm.predict(song_part), 5)
        mas_metrics.append(metric)
        text_metrics += str(metric) + '\n' + song_part + '\n\n'

    # Расчёт суммы метрик
    sum_metrics = 0
    for metriс in mas_metrics:
        sum_metrics += metriс

    # Если пользователь ничего не ввёл, то обрабатываем выход из программы
    if len(mas_metrics) == 0:
        return

    # Расчёт среденей метрики
    sr_metric = round(sum_metrics / len(mas_metrics), 5)

    # Запись в БД песни с метриками
    rq.add_song(name, text, text_metrics, sr_metric)

    # Добавляем новый текст в textEdit с метриками
    form.textEdit.setPlainText(f'{name}\n\n\n{text_metrics}')

    # Добавление в listWidget новой песни
    form.listWidget.addItem(name)

    # Вывод результатов в label
    if sr_metric < 0.5:
        form.label.setText(f'Метрика: {sr_metric}\nЕсть деструктив')
    else:
        form.label.setText(f'Метрика: {sr_metric}\nНет деструктива')
form.pushButton.clicked.connect(stratPredict)


# Функция открытия файла для загрузки в textEdit
def openFile():
    file_name, _ = QFileDialog.getOpenFileName(window, 'открыть файл', 'dev/examples', 'TXT File (*.txt)')
    if file_name:
        with open(file_name, 'r', encoding='utf8') as file:
            text = file.read()
        form.textEdit.setPlainText(text) 
form.pushButton_4.clicked.connect(openFile)


# Функция удаления выбранной песни
def deleteSong():
    current_item = form.listWidget.currentItem()
    if current_item == None:
        return
    
    name = current_item.text()
    rq.delete_song(name)

    index = form.listWidget.row(current_item)
    form.listWidget.takeItem(index)
    form.textEdit.clear()
form.pushButton_3.clicked.connect(deleteSong)


# При изменении textEdit удаляется значение текущей метрики
def change():
    form.label.clear()
form.textEdit.textChanged.connect(change)


# Функция выгрузки текста из файла в textEdit при нажатии на элемент listWidget
def chooseItem():
    name = form.listWidget.currentItem().text()

    text_metrics = rq.get_text_metrics(name)
    metric = rq.get_metric(name)

    form.textEdit.setPlainText(f'{name}\n\n\n{text_metrics}') 
    
    if metric < 0.5:
        form.label.setText(f'Метрика: {metric}\nЕсть деструктив')
    else:
        form.label.setText(f'Метрика: {metric}\nНет деструктива')
form.listWidget.clicked.connect(chooseItem)


app.exec()