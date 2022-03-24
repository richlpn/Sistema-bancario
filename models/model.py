from contextlib import contextmanager
from typing import List

from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from Settings import DATABASE_ENGINE, DATABASE_PATH

Engine = create_engine(DATABASE_ENGINE + ":///" + str(DATABASE_PATH))
Base = declarative_base(bind=Engine)

Session = sessionmaker(bind=Engine)


@contextmanager
def session_manager() -> Session:
    session = Session(expire_on_commit=False)
    try:
        yield session
    except Exception:
        session.rollback()
    finally:
        session.close()


class Model:

    @classmethod
    def all(cls) -> List:
        with session_manager() as session:
            return session.query(cls).all()

    @classmethod
    def get_by_id(cls, ID):
        cls_id = getattr(cls,"id")
        with session_manager() as session:
            return session.query(cls).filter(cls_id == ID).one_or_none()

    @classmethod
    def filter(cls, **kwargs) -> List:
        _key = list(kwargs.keys())[0]
        cls_filter = getattr(cls, _key)

        with session_manager() as session:
            return session.query(cls).filter(cls_filter == kwargs[_key]).all()

    def delete(self) -> bool:
        try:
            with session_manager() as session:
                session.delete(self)
                session.commit()
            return True
        except Exception as e:
            print(e)
            return False

    @classmethod
    def delete_all(cls):
        with session_manager() as session:
            session.query(cls).delete()
            session.commit()
        return True

    def save(self, commit=True):
        if not commit:
            return
        with session_manager() as session:
            session.add(self)
            session.commit()


def create_all():
    Base.metadata.create_all(Engine)
