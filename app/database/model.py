from sqlalchemy import create_engine, Column, Integer, String, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Настройка подключения к базе данных
engine = create_engine('sqlite:///db.sqlite3', echo=True)

# Настройка сессии для взаимодействия с базой данных
Session = sessionmaker(bind=engine)
session = Session()

# Базовый класс для определения моделей
Base = declarative_base()

# Определение модели данных
class Song(Base):
    __tablename__ = 'songs'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    text = Column(Text, nullable=False)
    text_metrics = Column(Text, nullable=False)
    metric = Column(Float, nullable=False)

# Создание таблицы
Base.metadata.create_all(engine)