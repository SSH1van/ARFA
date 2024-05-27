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

# Устанавливаем фиксированный размер окна
window.setFixedSize(window.size())

# Функция, которая вызывается при запуске программы
def formLoad():
    # Скрываем progressBar при запуске приложения
    form.progressBar.setVisible(False)
    
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
    if checkingUniqueness(lines): 
        form.result_label.setText('Песня уже проанализирована\nОбратитесь к списку справа')
        return
    
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
    if length < 11 and parts:
        parts[-1] = parts[-1] + current_part
    elif current_part != '':
        parts.append(current_part)

    # Удаляем из текста название песни
    text = text[len(name):].strip()

    # Включаем отображение processbar
    form.progressBar.setVisible(True)
    len_parts = len(parts)
    step = 100 / len_parts
    all_step = 0

    # Получаем метрику каждой части по 20 слов
    for song_part in parts:
        metric = round(gm.predict(song_part), 5)
        mas_metrics.append(metric)
        text_metrics += str(metric) + '\n' + song_part + '\n\n'

        form.progressBar.setValue(int(all_step)) 
        QtCore.QCoreApplication.processEvents()
        all_step += step

    # Выключаем отображение processbar
    form.progressBar.setVisible(False)

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

    # Добавляем новый текст в textEdit
    if form.show_metrics.isChecked():
        form.textEdit.setPlainText(f'{name}\n\n\n{text_metrics}')
    else:
        form.textEdit.setPlainText(f'{name}\n\n\n{text}')

    # Добавление в listWidget новой песни и выбор его
    form.listWidget.addItem(name)
    items = form.listWidget.findItems(name, QtCore.Qt.MatchExactly)
    form.listWidget.setCurrentItem(items[0])

    # Вывод результатов в label
    if sr_metric < 0.5:
        form.result_label.setText(f'Метрика: {sr_metric}\nЕсть деструктив')
    else:
        form.result_label.setText(f'Метрика: {sr_metric}\nНет деструктива')
form.start_button.clicked.connect(stratPredict)


# Функция открытия файла для загрузки в textEdit
def openFile():
    file_name, _ = QFileDialog.getOpenFileName(window, 'открыть файл', 'dev/examples', 'TXT File (*.txt)')
    if file_name:
        with open(file_name, 'r', encoding='utf8') as file:
            text = file.read()
        form.textEdit.setPlainText(text) 
form.open_file_button.clicked.connect(openFile)


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
form.delete_song_button.clicked.connect(deleteSong)


# При изменении textEdit удаляется значение текущей метрики
def change():
    form.result_label.clear()
form.textEdit.textChanged.connect(change)


# Функция выгрузки текста из файла в textEdit при нажатии на элемент listWidget
def chooseItem():
    name = form.listWidget.currentItem().text()

    text_metrics = rq.get_text_metrics(name)
    text = rq.get_text(name)
    metric = rq.get_metric(name)

    if form.show_metrics.isChecked():
        form.textEdit.setPlainText(f'{name}\n\n\n{text_metrics}')
    else:
        form.textEdit.setPlainText(f'{name}\n\n\n{text}')
    
    if metric < 0.5:
        form.result_label.setText(f'Метрика: {metric}\nЕсть деструктив')
    else:
        form.result_label.setText(f'Метрика: {metric}\nНет деструктива')
form.listWidget.clicked.connect(chooseItem)


# Функция изменения отображения/скрытия метрик песни
def changeCheckBox():
    if form.listWidget.currentItem() == None:
        return
    
    label = form.result_label.text()
    name = form.listWidget.currentItem().text()

    text_metrics = rq.get_text_metrics(name)
    text = rq.get_text(name)

    if form.show_metrics.isChecked():
        form.textEdit.setPlainText(f'{name}\n\n\n{text_metrics}')
    else:
        form.textEdit.setPlainText(f'{name}\n\n\n{text}')
    
    form.result_label.setText(label)
form.show_metrics.clicked.connect(changeCheckBox)


app.exec()