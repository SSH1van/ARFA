# Подключаем необходимые библиотеки
from keras.models import load_model
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import pickle

# Максимальная длинна части песни
max_review_len = 40

# Максимальное количесвто слов в словаре
num_words = 10000

global tokenizer
tokenizer = Tokenizer(num_words=num_words)
name = 'engine/my_dict.pkl'
with open(name, 'rb') as f:
    index = pickle.load(f)
tokenizer.word_index = index

global model
model = load_model('engine/best_model.h5')
    

# Функция получения строки, её формирование, предсказание и возврат
def predict(text):
    sequence = tokenizer.texts_to_sequences([text])
    data = pad_sequences(sequence, maxlen=max_review_len)
    result = model.predict(data)
   
    return(result[0][0])