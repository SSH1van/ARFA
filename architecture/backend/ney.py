# Подключаем необходимые библиотеки
from keras.models import load_model
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import pickle

# Количество слов в словаре
num_words = 10000
# Максимальная длинна сообщения (иначе обрежется или заполнится нуляи)
max_review_len = 100

#Загружаем в токенизатор словарь из файла 
tokenizer = Tokenizer(num_words=num_words)
name = 'engine/my_dict.pkl'
with open(name, 'rb') as f:
    index = pickle.load(f)
tokenizer.word_index = index

# Загружам обученную модель
model = load_model('engine/best_model.h5')
# Загружаем текст и приводим в необходимую форму
text = input("Введите текст для анализа: ")
sequence = tokenizer.texts_to_sequences([text])
data = pad_sequences(sequence, maxlen=max_review_len)
# Модель предсказывает
result = model.predict(data)

# Вывод тональности отзыва
print(result)
# Вывод предварительно результата
if result[[0]] < 0.5:
    print('Отзыв отрицательный')
else:
    print('Отзыв положительный')

input('Нажмите Enter для выхода\n')