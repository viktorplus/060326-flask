# l06_practice — схема проекта

## Что это

Практические задания к уроку 09.09.26 — два независимых скрипта, не связанных друг с другом:

| Файл | Тема | Заданий |
|---|---|---|
| `app.py` | модели Pydantic: валидаторы, `Field`, `Literal`, `ConfigDict` | 4 |
| `app2.py` | SQLAlchemy: движок, логирование SQL, модель `User` | 2 |

Ни Flask, ни HTTP здесь нет. Оба файла выполняются сверху вниз, «вход» зашит в код,
«выход» — печать в консоль.

Условия заданий: <https://lms.itcareerhub.de/pluginfile.php/20091/mod_resource/content/1/Django_Pr2.pdf>

## Точка входа и запуск

```
cd l06_practice
python app.py
python app2.py
```

Файлов на диске не создаётся ни тем, ни другим: `app.py` — это только модели Pydantic,
а `app2.py` по условию задания работает с базой **в оперативной памяти**
(`sqlite:///:memory:`), которая живёт ровно столько, сколько живёт процесс.

## Схема — app.py (Pydantic)

```mermaid
flowchart TB
    subgraph T1["Задание 1 — Event"]
        E["Event<br/>title: str<br/>date: datetime<br/>location: str"]
        EV["@field_validator('date')<br/>value < datetime.now() → ValueError<br/>'Дата события не может быть в прошлом'"]
        E --> EV
        ET["Проверка: date = now + 30 дней<br/>try/except ValueError → print"]
        EV --> ET
    end

    subgraph T2["Задание 2 — UserProfiles"]
        U["UserProfiles<br/>username: str<br/>password: str<br/>email: EmailStr"]
        UC["model_config = ConfigDict(<br/>str_strip_whitespace=True,<br/>str_min_length=2)"]
        UF["password: Field(..., min_length=8)<br/>строже общего str_min_length"]
        U --> UC
        U --> UF
        UT["user_profile2 = ('user2', '12345678', ...)<br/>→ print<br/>вариант с '12345' закомментирован"]
        UF --> UT
    end

    subgraph T3["Задание 3 — Transaction"]
        TR["Transaction<br/>amount: float Field(gt=0)<br/>currency: str max_length=3<br/>transaction_type: Literal['debit','credit']<br/>timestamp: datetime"]
        TT["transaction = (100.50, 'USD', 'credit', now)<br/>→ print"]
        TR --> TT
    end

    subgraph T4["Задание 4 — Appointment — НЕ ЗАВЕРШЕНО"]
        AP["Appointment<br/>appointment_date: datetime<br/>patient_name: str<br/>doctor_name: str"]
        AV["@field_validator('appointment_date')<br/>объявлен на уровне МОДУЛЯ,<br/>а не в теле класса<br/>→ Pydantic его не видит,<br/>модель принимает любую дату"]
        AP -.->|"связи нет<br/>из-за отступа"| AV
    end

    T1 --> Out["stdout: печать созданных моделей"]
    T2 --> Out
    T3 --> Out
```

## Схема — app2.py (SQLAlchemy)

```mermaid
flowchart TB
    L["logging.basicConfig(level=INFO)<br/>+ getLogger('sqlalchemy.engine').setLevel(INFO)<br/>второе обязательно: SQLAlchemy сама ставит<br/>своему логгеру WARNING при импорте"]
    E["engine = create_engine('sqlite:///:memory:')<br/>база в оперативной памяти,<br/>как требует условие"]
    B["Base = declarative_base()<br/>стиль SQLAlchemy 1.x"]
    U["class User(Base)<br/>__tablename__ = 'users'<br/>id PK, name VARCHAR(50), age INT"]
    B --> U
    C["Base.metadata.create_all(engine)<br/>CREATE TABLE users"]
    U --> C
    E --> C
    S["with Session() as session<br/>INSERT admin/20 + COMMIT<br/>затем SELECT"]
    C --> S
    L -.->|"включает вывод"| C
    S --> Out["В консоли: BEGIN, CREATE TABLE,<br/>INSERT с параметрами, COMMIT, SELECT<br/>+ print строки из базы"]
```

## Вход / Выход

| Скрипт | Вход | Выход |
|---|---|---|
| `app.py` | значения зашиты в код: `now + 30 дней`, `('user2', '12345678', 'user@example.com')`, `(100.50, 'USD', 'credit', now)` | три строки в stdout — представления `Event`, `UserProfiles`, `Transaction` |
| `app2.py` | ничего | ничего: ни файла, ни лога |

## Связи

`app.py` и `app2.py` друг друга не импортируют и общих данных не имеют. `__init__.py` пустой.

Внешние зависимости: `pydantic`, `email-validator` (для `EmailStr`), `sqlalchemy`.

## Особенности и незакрытые задания

* **Задание 4 не работало из-за отступа — исправлено.** Декоратор `@field_validator` и функция
  стояли на уровне модуля, а не в теле класса `Appointment`. Pydantic собирает валидаторы
  только из тела класса, поэтому проверка никогда не вызывалась: модель молча принимала любую
  дату, включая прошедшую. Ни ошибки, ни предупреждения — самый неприятный вид бага.
  Достаточно было сдвинуть декоратор и функцию на один уровень вправо.
* **Там же вторая ошибка: валидатор не возвращал `value`.** Даже перенесённый в класс, он
  записал бы в поле `None`, и модель «прошла» бы проверку с пустой датой. Валидатор обязан
  вернуть значение.
* Условие приведено к тексту задания («не раньше текущей даты и времени») — раньше проверка
  была строже, требовала запись минимум за 24 часа. Добавлены две проверки: дата в прошлом
  отвергается, дата в будущем проходит.
* **Задание в `app2.py` доведено до конца.** Требовалась база в памяти и вывод логов всех
  операций; было ни того, ни другого. Исправлены три отдельные вещи:
  1. `sqlite:///base.db` → `sqlite:///:memory:` — по условию база должна жить в памяти,
     а не копить файл в рабочем каталоге.
  2. Появились `Base.metadata.create_all(engine)` и сессия с `INSERT`/`SELECT`.
     Без единой операции логировать нечего: `create_engine` соединение **не открывает**,
     он только настраивает пул.
  3. Логирование действительно включено. Прежний комментарий утверждал, что логгер
     `sqlalchemy.engine` унаследует уровень от корневого и настраивать его отдельно не нужно —
     **это неверно**: при импорте SQLAlchemy сама выставляет логгеру `sqlalchemy` уровень
     `WARNING`, и цепочка наследования обрывается на нём. Одного `logging.basicConfig(INFO)`
     не хватает, нужен явный
     `logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)` — как в
     [`l04_orm_basics/app_1.py`](../l04_orm_basics/SCHEMA.md) — либо `echo=True` у движка.
     Проверить самому: `logging.getLogger('sqlalchemy').level` → `30`.
* **`except ValueError` в задании 1 ловит и `ValidationError`** — она наследник `ValueError`.
* **Неиспользуемый `DECIMAL` из SQLAlchemy удалён** из `app.py`. Замечание в комментарии у поля
  `amount` при этом верное и осталось: для денег `float` неточен (`0.1 + 0.2 != 0.3`),
  в рабочем коде берут `decimal.Decimal` — это другой, стандартный модуль.
* **`datetime.now()` — наивное время без часового пояса.** Сравнение наивной даты с aware-датой
  бросает `TypeError: can't compare offset-naive and offset-aware datetimes`. Раньше это было
  учтено только в задании 4; теперь в обоих валидаторах стоит
  `datetime.now(value.tzinfo) if value.tzinfo else datetime.now()`.
* **Внутренний класс `ConfigDict` в `UserProfiles` был бы проигнорирован**: старый способ
  требует имя `Config`. Актуальный вариант — атрибут `model_config`, он и используется.
* **`declarative_base()` в `app2.py` — стиль 1.x.** В остальных файлах проекта используется
  класс `DeclarativeBase` из SQLAlchemy 2.0; результат одинаковый, но 2.0-стиль предпочтителен.
