pip install SQLAlchemy

'<DBMS>+<library>://<user>:<password>@<host>:<port>/<database>'
'mysql+pymysql://user:password@localhost:3306/mydatabase'

from sqlalchemy import create_engine
# PostgreSQL
engine = create_engine('postgresql://user:password@localhost:5432/mydatabase')
# MySQL
engine = create_engine('mysql+pymysql://user:password@localhost:3306/mydatabase')
# SQLite (для локального файла)
engine = create_engine('sqlite:///path/to/database.db')
# SQLite (в оперативной памяти)
engine = create_engine('sqlite:///:memory:')

| База данных          | Python ORM            |
| -------------------- | --------------------- |
| таблица `employees`  | класс `Employee`      |
| столбец `first_name` | атрибут `first_name`  |
| строка таблицы       | экземпляр `Employee`  |
| внешний ключ         | связь между объектами |

SQLAlchemy предоставляет два связанных инструмента:

- **Core** — построение SQL-выражений через Python-объекты таблиц и выражений;
- **ORM** — работа с классами, экземплярами и отношениями.

Оба используют `Engine`, который знает, к какой базе и через какой драйвер обращаться.