from app.database.model import session
from app.database.model import Song
from sqlalchemy import String, Float, Text



def add_song(name: String, text: Text, text_metrics: Text, metric: Float) -> None:
    new_record = Song(name=name, text=text, text_metrics=text_metrics, metric=metric)
    session.add(new_record)
    session.commit()



def delete_song(name: String):
    record = session.query(Song).filter_by(name=name).first()
    session.delete(record)
    session.commit()



def get_text(name: String) -> String:
    record = session.query(Song).filter_by(name=name).first()
    return record.text

def get_text_metrics(name: String) -> String:
    record = session.query(Song).filter_by(name=name).first()
    return record.text_metrics

def get_metric(name: String) -> String:
    record = session.query(Song).filter_by(name=name).first()
    return record.metric

def get_all_names() -> list:
    names = session.query(Song.name).all()
    return [name[0] for name in names]