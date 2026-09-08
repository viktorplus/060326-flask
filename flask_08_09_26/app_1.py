import logging

from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('sqlalchemy.engine')
logger.setLevel(logging.DEBUG)



class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    # id = Column(Integer, primary_key=True)
    # name = Column(String)
    # email = Column(String)

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30))
    age: Mapped[int] = mapped_column(Integer)


engine = create_engine('sqlite:///db.sqlite3')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

with Session() as session:
    new_user = User(id=6, username='admin', age='tyututu20') #!
    session.add(new_user)
    session.commit()






