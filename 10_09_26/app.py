# Урок 10.09.26: агрегатные функции (avg, count), группировка GROUP BY и псевдонимы таблиц.
# Модели те же, что и 09.09.26, — новое здесь только в блоке запросов внизу файла.

from sqlalchemy import create_engine, Integer, String, ForeignKey

# label — присвоить вычисляемой колонке имя (AS ...); в этом файле импортирован, но не используется.
from sqlalchemy import select, label

from sqlalchemy import and_, or_, not_, desc

# func — «мост» к SQL-функциям: func.avg(...), func.count(...), func.max(...).
from sqlalchemy import func

# aliased — псевдоним таблицы (SQL AS), нужен для самосоединений и читаемости запроса.
from sqlalchemy.orm import aliased

from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, relationship


# Базовый класс моделей.
class Base(DeclarativeBase):
    pass


# Сторона «один».
class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(30))
    age: Mapped[int] = mapped_column(Integer)

    # Варианты кардинальности связи (оставлены для сравнения):
    # addresses: Mapped['Address'] = relationship(back_populates='user') # 1:1
    # addresses: Mapped[Optional['Address']] = relationship(back_populates='user')  # 1:1 or None

    # Действующий вариант: один пользователь — много адресов.
    addresses: Mapped[list['Address']] = relationship(back_populates='user') # 1: M

    # Представление для print().
    def __str__(self) -> str:
        return f'User: {self.username}; {self.age}'

    # Представление внутри списков и в отладчике.
    def __repr__(self) -> str:
        return f'User: {self.username}; {self.age}'


# Сторона «многие».
class Address(Base):
    __tablename__ = 'addresses'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    description: Mapped[str] = mapped_column(String(100))

    # Внешний ключ на users.id — связь на уровне БД.
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    # Обратная сторона связи; lazy='joined' подтягивает User сразу через LEFT OUTER JOIN.
    user: Mapped['User'] = relationship(back_populates='addresses', lazy='joined')

# Подключение к той же базе, что и в уроке 09.09 (файл в текущем рабочем каталоге).
engine = create_engine('sqlite:///db.sqlite')
# Создаём недостающие таблицы.
Base.metadata.create_all(engine)
# Фабрика сессий.
Session = sessionmaker(bind=engine)


with Session() as session:
    # SELECT avg(age) FROM users — запрос возвращает ровно одно значение.
    query = select(func.avg(User.age))
    # session.scalar() — сокращение для «взять первую строку и её первую колонку».
    # Для агрегатов это удобнее, чем scalars(...).one().
    result = session.scalar(query)
    print(result)

    # SELECT username, count(id) FROM users GROUP BY username.
    # Правило SQL: всё, что не под агрегатной функцией, должно быть в GROUP BY.
    query = select(User.username, func.count(User.id)).group_by(User.username)
    # Здесь нужен execute, а не scalars: в результате ДВЕ колонки,
    # scalars вернул бы только первую и count потерялся бы.
    result = session.execute(query).all()
    # .all() даёт список кортежей Row вида ('username123', 1).
    print(result)

    # Псевдоним таблицы users. В SQL это "FROM users AS user_aliase".
    # Практический смысл: без псевдонима нельзя дважды сослаться на одну таблицу
    # в одном запросе (самосоединение, сравнение строк таблицы между собой).
    user_aliase = aliased(User, name='user_aliase')

    # Тот же запрос с группировкой, но обращения идут через псевдоним, а не через User.
    # Результат идентичен предыдущему — здесь это демонстрация синтаксиса.
    stmt = select(user_aliase.username, func.count(user_aliase.id)).group_by(user_aliase.username)
    result = session.execute(stmt).all()
    print(result)
