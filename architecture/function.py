# Подключаем необходимые библиотеки
from keras.models import load_model
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import pickle

# Максимальная длинна части песни
max_review_len = 100

# Функция загрузки словаря и обученной модели
# ДАЙ БОГ сил этому коду, чтобы эта функция отработала и потом все эти значения сохранились иначе пизда
num_words = 10000

global tokenizer
tokenizer = Tokenizer(num_words=num_words)
name = 'engine/my_dict.pkl'
with open(name, 'rb') as f:
    index = pickle.load(f)
tokenizer.word_index = index

global model
model = load_model('engine/best_model.h5')
    

# Функция получения строки, её формирование, предсказание и вывод
def predict(text):
    sequence = tokenizer.texts_to_sequences([text])
    data = pad_sequences(sequence, maxlen=max_review_len)
    result = model.predict(data)
   
    # Тут будешь получать тональность в формате [[0.16969028]] (ЭТО ЕЩЁ И МАССИВ В МАССИВЕ, УДАЧИ, БРАТ) 
    # и потом в крестах считать среденне значение
    return(result[0][0])