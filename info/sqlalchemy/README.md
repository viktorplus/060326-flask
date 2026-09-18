# SQLAlchemy 2.0 — справочник

Библиотека работы с базами данных. Два уровня, которые важно не путать:

* **Core** — таблицы и SQL-выражения (`Table`, `Column`, `select`);
* **ORM** — классы-модели поверх Core (`DeclarativeBase`, `relationship`, `Session`).

Установка: `python -m pip install SQLAlchemy`

В этом репозитории SQLAlchemy используется в пяти уроках:

| Урок | Тема |
|---|---|
| `l04_orm_basics` | движок, первая модель, сессия, INSERT, три способа маппинга |
| `l05_orm_relationships` | `ForeignKey` + `relationship`, `SELECT ... WHERE`, операторы |
| `l06_practice` | практика: движок, логирование, модель |
| `l07_orm_aggregates` | `func`, `GROUP BY`, `aliased` |
| `l08_orm_loading` | стратегии `lazy`, проблема N+1, `HAVING`, подзапросы, `JOIN` |

Запуск любого — из каталога урока: `cd l05_orm_relationships && python app.py`

**Три вещи, которые экономят часы отладки.**

1. `create_engine` НЕ открывает соединение — он только настраивает пул. Пока не выполнена
   реальная операция, в логе пусто, и кажется, что «логирование не включилось».
2. Логгер SQLAlchemy при импорте сам ставит себе уровень `WARNING`. Одного
   `logging.basicConfig(level=INFO)` мало — нужен явный
   `logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)` либо `echo=True` у движка.
3. Относительный путь в строке подключения разрешается от рабочего каталога процесса,
   а не от файла скрипта. Запуск не из того каталога молча создаёт пустую базу.

## Статьи

### Движок и схема

| Символ | О чём | Где в коде уроков |
|---|---|---|
| [`create_engine`](create_engine.md) | Создаёт «движок» — точку входа в базу: пул соединений плюс диалект конкретной СУБД. | `l04_orm_basics/app_1.py:9`<br>`l04_orm_basics/app_1.py:59` |
| [`create_all`](create_all.md) | Создаёт в базе все таблицы, описанные наследниками `Base`, которых там ещё нет. | `l04_orm_basics/app_1.py:63`<br>`l04_orm_basics/app_2.py:101` |
| [`String`](String.md) | Типы колонок SQL. | `l04_orm_basics/app_1.py:9`<br>`l04_orm_basics/app_1.py:53` |
| [`Column`](Column.md) | Описание колонки в стиле SQLAlchemy 1. | `l04_orm_basics/app_1.py:45`<br>`l04_orm_basics/app_1.py:46` |
| [`Table`](Table.md) | Описание таблицы объектом, без класса модели. | `l04_orm_basics/app_2.py:20`<br>`l04_orm_basics/app_2.py:63` |
| [`registry`](registry.md) | Реестр соответствий «класс — таблица». | `l04_orm_basics/app_2.py:18` |
| [`automap_base`](automap_base.md) | Строит классы моделей автоматически, прочитав схему уже существующей базы. | `l04_orm_basics/app_2.py:11`<br>`l04_orm_basics/app_2.py:10` |

### Модели

| Символ | О чём | Где в коде уроков |
|---|---|---|
| [`DeclarativeBase`](DeclarativeBase.md) | Базовый класс для моделей в стиле SQLAlchemy 2. | `l04_orm_basics/app_1.py:14`<br>`l04_orm_basics/app_1.py:34` |
| [`declarative_base`](declarative_base.md) | Функция-фабрика базового класса в стиле SQLAlchemy 1. | `l06_practice/app2.py:9`<br>`l06_practice/app2.py:44` |
| [`Mapped`](Mapped.md) | Аннотация типа для колонки: `Mapped[int]`, `Mapped[str]`, `Mapped[list['Address']]`. | `l04_orm_basics/app_1.py:14`<br>`l04_orm_basics/app_1.py:51` |
| [`mapped_column`](mapped_column.md) | Описывает параметры колонки: первичный ключ, длину, внешний ключ, значение по умолчанию. | `l04_orm_basics/app_1.py:14`<br>`l04_orm_basics/app_1.py:51` |
| [`relationship`](relationship.md) | Связь на уровне ORM: питоновский атрибут-объект вместо колонки с числом. | `l05_orm_relationships/app.py:21`<br>`l05_orm_relationships/app.py:48` |
| [`ForeignKey`](ForeignKey.md) | Внешний ключ — связь на уровне базы данных: «в этой колонке лежит id из той таблицы». | `l05_orm_relationships/app.py:11`<br>`l05_orm_relationships/app.py:72` |

### Сессия и выполнение

| Символ | О чём | Где в коде уроков |
|---|---|---|
| [`sessionmaker`](sessionmaker.md) | Фабрика сессий, привязанная к движку. | `l04_orm_basics/app_1.py:14`<br>`l04_orm_basics/app_1.py:66` |
| [`session.add`](session_add.md) | Помечает объект как новый в сессии. | `l04_orm_basics/app_1.py:82`<br>`l06_practice/app2.py:77` |
| [`session.commit`](session_commit.md) | `commit()` отправляет накопленные изменения в базу и фиксирует транзакцию. | `l04_orm_basics/app_1.py:86`<br>`l06_practice/app2.py:78` |
| [`session.get`](session_get.md) | Находит объект по первичному ключу. | `l05_orm_relationships/app.py:206`<br>`l09_orm_practice/app.py:110` |
| [`session.scalars`](session_scalars.md) | Выполняет запрос и возвращает ПЕРВУЮ КОЛОНКУ каждой строки. | `l05_orm_relationships/app.py:187`<br>`l05_orm_relationships/app.py:199` |
| [`session.execute`](session_execute.md) | Выполняет запрос и возвращает строки целиком — объекты `Row`, похожие на именованные кортежи. | `l07_orm_aggregates/app.py:79`<br>`l07_orm_aggregates/app.py:91` |
| [`session.scalar`](session_scalar.md) | Выполняет запрос и возвращает ОДНО значение — первую колонку первой строки. | `l05_orm_relationships/app.py:187`<br>`l05_orm_relationships/app.py:199` |
| [`first / one / one_or_none / all`](first_one_all.md) | Четыре способа забрать результат. | `l05_orm_relationships/app.py:187`<br>`l05_orm_relationships/app.py:199` |

### Построение запроса

| Символ | О чём | Где в коде уроков |
|---|---|---|
| [`select`](select.md) | Конструктор SELECT-запроса в стиле SQLAlchemy 2. | `l05_orm_relationships/app.py:171`<br>`l05_orm_relationships/app.py:216` |
| [`.where()`](where.md) | Добавляет к запросу условие `WHERE`. | `l05_orm_relationships/app.py:199`<br>`l05_orm_relationships/app.py:210` |
| [`.order_by()`](order_by.md) | Задаёт порядок строк в результате. | `l05_orm_relationships/app.py:261`<br>`l05_orm_relationships/app.py:266` |
| [`.join()`](join.md) | Соединяет таблицы в запросе. | `l08_orm_loading/app.py:155`<br>`l08_orm_loading/app.py:149` |
| [`.distinct()`](distinct.md) | Убирает из результата повторяющиеся строки — SQL-конструкция `DISTINCT`. | `l08_orm_loading/app.py:155`<br>`l08_orm_loading/app.py:151` |

### Операторы фильтрации

| Символ | О чём | Где в коде уроков |
|---|---|---|
| [`or_ / and_ / not_`](or_.md) | Логические операторы для условий SQL. | `l05_orm_relationships/app.py:246`<br>`l05_orm_relationships/app.py:251` |
| [`.ilike() / .like()`](ilike.md) | Поиск по шаблону. | `l05_orm_relationships/app.py:227`<br>`l05_orm_relationships/app.py:246` |
| [`.in_()`](in_.md) | Условие «значение входит в список»: SQL-оператор `IN`. | `l05_orm_relationships/app.py:240` |
| [`.between()`](between.md) | Условие «значение в диапазоне», границы ВКЛЮЧИТЕЛЬНО. | `l05_orm_relationships/app.py:232` |

### Агрегаты и группировка

| Символ | О чём | Где в коде уроков |
|---|---|---|
| [`func`](func.md) | «Мост» к SQL-функциям: `func. | `l07_orm_aggregates/app.py:68`<br>`l07_orm_aggregates/app.py:76` |
| [`.group_by()`](group_by.md) | Группирует строки по значению колонки, чтобы применить к каждой группе агрегат. | `l07_orm_aggregates/app.py:76`<br>`l07_orm_aggregates/app.py:90` |
| [`.having()`](having.md) | Фильтрует УЖЕ СГРУППИРОВАННЫЕ строки по значению агрегата. | `l08_orm_loading/app.py:120` |
| [`.label()`](label.md) | Даёт имя вычисляемой колонке — это SQL-конструкция `AS`. | `l08_orm_loading/app.py:107`<br>`l08_orm_loading/app.py:108` |
| [`aliased`](aliased.md) | Псевдоним таблицы — SQL-конструкция `AS`. | `l07_orm_aggregates/app.py:12`<br>`l07_orm_aggregates/app.py:86` |
| [`scalar_subquery`](scalar_subquery.md) | Превращает запрос в подзапрос, возвращающий ОДНО значение, — его можно подставить прямо в условие. | `l08_orm_loading/app.py:125`<br>`l08_orm_loading/app.py:127` |

### Сложные запросы

| Символ | О чём | Где в коде уроков |
|---|---|---|
| [`exists / any / has`](exists.md) | Условие «существует хотя бы одна связанная строка». | — |
| [`case`](case.md) | Условное выражение внутри запроса — SQL-конструкция `CASE WHEN . | — |
| [`subquery`](subquery.md) | Превращает запрос в подзапрос, к которому можно присоединиться как к таблице. | — |
| [`cte`](cte.md) | Обобщённое табличное выражение — SQL `WITH имя AS (. | — |
| [`union / union_all`](union.md) | Объединение результатов нескольких запросов в один набор строк. | — |
| [`over — оконные функции`](over.md) | Оконная функция: считает агрегат, **не схлопывая строки**. | — |

### Постранично и массово

| Символ | О чём | Где в коде уроков |
|---|---|---|
| [`.limit() / .offset()`](limit_offset.md) | Ограничение количества строк и пропуск первых N. | `l09_orm_practice/app.py:128`<br>`l09_orm_practice/app.py:138` |
| [`update() / delete() — массовые`](bulk_update_delete.md) | Изменение и удаление строк ОДНИМ запросом, без загрузки объектов в память. | — |
| [`session.delete`](session_delete.md) | Помечает объект на удаление. | `l09_orm_practice/app.py:101`<br>`l09_orm_practice/app.py:94` |

### Загрузка связей

| Символ | О чём | Где в коде уроков |
|---|---|---|
| [`lazy (стратегии загрузки)`](lazy.md) | Стратегия загрузки связи: КОГДА и СКОЛЬКИМИ запросами подтягиваются связанные объекты. | `l05_orm_relationships/app.py:77`<br>`l07_orm_aggregates/app.py:56` |

### Исключения

| Символ | О чём | Где в коде уроков |
|---|---|---|
| [`NoResultFound`](NoResultFound.md) | Исключения, которыми `. | `l05_orm_relationships/app.py:24`<br>`l05_orm_relationships/app.py:201` |
| [`IntegrityError`](IntegrityError.md) | Исключение при нарушении ограничения базы: уникальность, внешний ключ, `NOT NULL`. | — |

## Примеры

Запускаемые примеры: `cd info/sqlalchemy && python examples.py`
