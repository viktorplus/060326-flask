# Индекс проектов и схема связей

Учебный репозиторий курса по Flask. Каждый каталог — отдельное занятие, названное по дате.
Проекты **независимы**: ни один из них не импортирует другой, общего кода и общей базы нет.
Связывает их только линия обучения — каждая следующая тема опирается на предыдущую.

Подробная схема каждого проекта лежит рядом с его кодом, в файле `SCHEMA.md`.

## Индекс

| Каталог | Тема занятия | Стек | Тип | Точка входа | Схема |
|---|---|---|---|---|---|
| `flask0` | маршрутизация, конвертеры путей | Flask | веб-сервер | `python flask0/app.py` | [SCHEMA](flask0/SCHEMA.md) |
| `flask_03_09_26` | Pydantic: модели, валидаторы, `Response` | Flask + Pydantic | веб-сервер | `cd flask_03_09_26 && python app.py` | [SCHEMA](flask_03_09_26/SCHEMA.md) |
| `flask_04_09_26` | REST API «сотрудники», слои, хранение в JSON | Flask + Pydantic + dotenv | **REST API** | `python -m flask_04_09_26.app` | [SCHEMA](flask_04_09_26/SCHEMA.md) |
| `flask_08_09_26` | первые модели ORM, 3 способа маппинга | SQLAlchemy | скрипт | `python flask_08_09_26/app_1.py` (и `app_2.py`) | [SCHEMA](flask_08_09_26/SCHEMA.md) |
| `flask_09_09_26` | `relationship` 1:M, фильтры `WHERE` | SQLAlchemy | скрипт | `cd flask_09_09_26 && python app.py` | [SCHEMA](flask_09_09_26/SCHEMA.md) |
| `flask_09_09_26_practic` | практика: 4 задания Pydantic + 2 SQLAlchemy | Pydantic, SQLAlchemy | скрипт | `python flask_09_09_26_practic/app.py` (и `app2.py`) | [SCHEMA](flask_09_09_26_practic/SCHEMA.md) |
| `10_09_26` | агрегаты, `GROUP BY`, `aliased` | SQLAlchemy | скрипт | `cd 10_09_26 && python app.py` | [SCHEMA](10_09_26/SCHEMA.md) |
| `11_09_26` | стратегии `lazy`, N+1, `HAVING`, подзапросы | SQLAlchemy | скрипт | `cd 11_09_26 && python app.py` | [SCHEMA](11_09_26/SCHEMA.md) |

Flask есть только в первых трёх проектах. Начиная с 08.09 занятия про базу данных, и веб-слоя
в них нет вообще — это обычные скрипты, которые выполняются сверху вниз и завершаются.

## Схема связей

```mermaid
flowchart TB
    subgraph line1["Линия 1 · HTTP и Flask"]
        direction LR
        F0["flask0<br/>маршруты, конвертеры<br/>состояния нет"]
        F03["flask_03_09_26<br/>+ Pydantic<br/>+ ручной Response"]
        F04["flask_04_09_26<br/>REST API, слои,<br/>хранение на диске"]
        F0 -->|"добавили валидацию<br/>входного JSON"| F03
        F03 -->|"добавили слои,<br/>хранилище и коды ответа"| F04
    end

    subgraph line2["Линия 2 · Pydantic"]
        direction LR
        P1["flask_03_09_26/models.py<br/>Field, ConfigDict,<br/>field_validator, наследование"]
        P2["flask_04_09_26/schemas.py<br/>+ model_validator<br/>+ computed_field<br/>+ TypeAdapter"]
        P3["flask_09_09_26_practic/app.py<br/>практика: 4 задания"]
        P1 --> P2
        P1 --> P3
    end

    subgraph line3["Линия 3 · SQLAlchemy"]
        direction LR
        S1["flask_08_09_26<br/>модель = таблица,<br/>create_all, сессия, INSERT"]
        S2["flask_09_09_26<br/>ForeignKey + relationship<br/>SELECT ... WHERE"]
        S3["10_09_26<br/>avg, count, GROUP BY,<br/>aliased"]
        S4["11_09_26<br/>lazy-стратегии, N+1,<br/>HAVING, подзапросы, JOIN"]
        S5["flask_09_09_26_practic/app2.py<br/>практика: движок и модель"]
        S1 -->|"появилась связь<br/>между таблицами"| S2
        S2 -->|"агрегаты"| S3
        S3 -->|"как это грузится<br/>и сколько стоит"| S4
        S1 --> S5
    end

    F03 -.->|"тот же модуль"| P1
    F04 -.->|"тот же модуль"| P2

    line1 --> Deps
    line2 --> Deps
    line3 --> Deps

    subgraph Deps["Внешние зависимости"]
        D1["flask"]
        D2["pydantic + email-validator"]
        D3["python-dotenv"]
        D4["sqlalchemy + sqlite3"]
    end

    subgraph Data["Данные на диске"]
        J1[("flask_04_09_26/<br/>employees_data.json<br/>пишется приложением")]
        J2["employee.json<br/>list_employees.json<br/>примеры тел запросов"]
        B1[("flask_09_09_26/db.sqlite<br/>users 21 · addresses 0")]
        B2[("10_09_26/db.sqlite<br/>users 21 · addresses 0")]
        B3[("11_09_26/db.sqlite<br/>users 15 · addresses 15<br/>другая схема!")]
        B4["db.sqlite3 / base.db<br/>создаются в рабочем каталоге,<br/>в репозитории их нет"]
    end

    F04 --> J1
    F04 -.- J2
    S2 --> B1
    S3 --> B2
    S4 --> B3
    S1 --> B4
    S5 --> B4

    ENV[".env в корне<br/>USERNAME, DRIVER"] -.->|"единственный потребитель"| F04
```

## Кто чем связан на самом деле

| Вопрос | Ответ |
|---|---|
| Импортируют ли проекты друг друга? | **Нет.** Ни одного межпроектного импорта. Единственные внутренние импорты — внутри `flask_03_09_26` (`app.py → models.py`) и внутри `flask_04_09_26` (`app.py → schemas.py → utils.py → settings.py`) |
| Общая база данных? | **Нет.** Три отдельных файла `db.sqlite` в трёх каталогах. У `11_09_26` вдобавок **другая схема**: `users.name` вместо `username`, `addresses.city` вместо `description` |
| Общий файл конфигурации? | Корневой `.env` читает только `flask_04_09_26` |
| Общий код между линиями? | Нет, каждая тема начинается с нуля. Модели `User`/`Address` объявлены заново в четырёх файлах |

## Сводка: вход и выход

| Проект | Вход | Выход |
|---|---|---|
| `flask0` | только путь URL | `text/html`, строка |
| `flask_03_09_26` | путь URL; JSON для `/` зашит в код | `application/json` + `text/html` |
| `flask_04_09_26` | тело HTTP-запроса (JSON), `.env` | `application/json`, коды `200/201/400`; запись в `employees_data.json` |
| `flask_08_09_26` | данные зашиты в код | файл SQLite + SQL-лог в консоли |
| `flask_09_09_26` | `db.sqlite`; параметры запросов зашиты в код | stdout, базу не меняет |
| `flask_09_09_26_practic` | значения зашиты в код | stdout (`app.py`); `app2.py` не выводит ничего |
| `10_09_26` | `db.sqlite` | stdout, базу не меняет |
| `11_09_26` | `db.sqlite` | stdout + весь SQL (`echo=True`), базу не меняет |

Данные извне принимает **только `flask_04_09_26`**. У остальных вход зашит в исходник либо
лежит в файле БД рядом.

## Общие грабли: рабочий каталог

Во всех проектах пути относительные, а значит разрешаются от **текущего каталога процесса**,
а не от расположения файла. Запуск не из того каталога не выдаёт ошибку — он молча создаёт
пустую базу или пишет JSON не туда.

| Проект | Откуда запускать | Почему |
|---|---|---|
| `flask_03_09_26` | из каталога проекта | абсолютный импорт `from models import User` |
| `flask_04_09_26` | из корня репозитория | относительные импорты пакета + `DATA_FILE = "flask_04_09_26/..."` |
| `flask_09_09_26`, `10_09_26`, `11_09_26` | из каталога проекта | готовый `db.sqlite` лежит внутри каталога |
| `flask0`, `flask_08_09_26`, `flask_09_09_26_practic` | откуда угодно | файлов данных не читают (БД создадут в текущем каталоге) |

Каталоги `10_09_26` и `11_09_26` начинаются с цифры — это недопустимый идентификатор Python,
поэтому `import 10_09_26.app` не работает и файлы запускаются только напрямую. Лежащие там
`__init__.py` формально бесполезны.

## Что ещё есть в репозитории

* **`.github/workflows/main.yml`** — workflow «Сохранить урок преподавателя». Запускается вручную
  с вкладки Actions, создаёт в этом репозитории ветку `teacher/<метка времени UTC>` со снимком
  ветки `main` репозитория преподавателя (`cpython-projects/060326-flask`). К коду уроков
  отношения не имеет — это инструмент архивации.
* **`.env`** — `USERNAME` и `DRIVER`. Читается только в `flask_04_09_26/app.py`, причём под
  другим именем (`DB_USERNAME`), то есть сейчас туда приходит `None`.
* **`.idea/`** — настройки PyCharm, в том числе подключённые источники данных.

## Как смотреть эти схемы

Диаграммы написаны на **Mermaid** — в блоках кода с языком `mermaid`.

* **PyCharm** — плагин *Mermaid* (JetBrains) уже входит в сборку 2026.2.1 и включён.
  Откройте любой `SCHEMA.md` и включите предпросмотр Markdown: кнопка в правом верхнем углу
  редактора либо `Ctrl+Shift+A` → `Markdown Preview`.
* **GitHub** — рендерит Mermaid в `.md` сам, ничего включать не нужно.
