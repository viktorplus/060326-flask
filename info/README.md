# Справочник по библиотекам курса

Разбор каждой функции, которая участвует в коде этого репозитория, плюс популярные соседи,
которых в уроках нет, но которые понадобятся дальше.

Ссылки «Где в репозитории» охватывают обе серии каталогов: уроки `l…` и практику `p…`.

## Что где лежит

| Каталог | Пакет | Статей | Что внутри |
|---|---|---|---|
| [`flask/`](flask/README.md) | `flask` | 13 | приложение, маршруты, запрос, ответ, ошибки |
| [`pydantic/`](pydantic/README.md) | `pydantic` | 16 | модели, поля, валидаторы, сериализация |
| [`sqlalchemy/`](sqlalchemy/README.md) | `SQLAlchemy` | 48 | движок, модели, сессия, запросы, связи, **сложные запросы** |
| [`dotenv/`](dotenv/README.md) | `python-dotenv` | 4 | чтение и запись `.env` |
| [`github-actions/`](github-actions/README.md) | GitHub Actions | 14 | разбор `.github/workflows/main.yml` по директивам |
| [`git/`](git/README.md) | `git` | 9 | команды из workflow + **как скопировать репозиторий в отдельную ветку** |

В корне этого каталога лежат **исходные конспекты с занятий** — они не тронуты:

* `SQLAlchemy.md` — строка подключения и установка;
* `mapping` — три способа связать класс с таблицей;
* `computed_field.md` — валидаторы и вычисляемые поля;
* `default_factory.md` — значение по умолчанию против фабрики;
* `model_dump__model_validate` — какой метод что возвращает;
* `type_adapter.md` — зачем нужен `TypeAdapter`;
* `responce.md` — сценарий обработки POST-запроса;
* `run-install.txt` — установка зависимостей и способы запуска Flask.

Справочник в подкаталогах их не заменяет, а разворачивает.

## Как устроена статья

Все статьи написаны по одному шаблону, поэтому их можно листать и сравнивать:

1. **Что это** — одна-две фразы.
2. **Зачем** — какую задачу решает и почему без этого хуже.
3. **Сигнатура** и **таблица параметров** — что можно передать и что будет по умолчанию.
4. **Минимальный пример** — с выводом, если он показателен.
5. **Типичные задачи** — готовые рецепты под частые случаи.
6. **Частые ошибки** — самый ценный раздел, см. ниже.
7. **Где в репозитории** — точные ссылки `файл:строка` на код уроков.
8. **См. также** — соседние статьи.

## Раздел «Частые ошибки» — чем он отличается от чужих справочников

Туда попали не абстрактные предупреждения, а ошибки, которые **реально были в коде этого
репозитория** и которые мы чинили с проверкой запуском. По каждой известно точное поведение:
текст исключения, код ответа, число запросов к базе.

| Ошибка | Где была | Статья |
|---|---|---|
| `jsonify(e.errors)` — передан объект метода | `l02_pydantic_models` | [errors](pydantic/errors.md) |
| `jsonify(e.errors())` — в `ctx` несериализуемый `ValueError` | `l02_pydantic_models` | [errors](pydantic/errors.md) |
| Демонстрация в модуле моделей выполнялась при импорте | `l02_pydantic_models` | [BaseModel](pydantic/BaseModel.md) |
| Ключ `.env` совпал с системным `USERNAME` | `l03_rest_api` | [load_dotenv](dotenv/load_dotenv.md) |
| `User(id=6, ...)` — второй запуск падал | `l04_orm_basics` | [IntegrityError](sqlalchemy/IntegrityError.md) |
| `.first()` без проверки на `None` | `l05_orm_relationships` | [first / one / all](sqlalchemy/first_one_all.md) |
| Валидатор объявлен вне тела класса | `l06_practice` | [field_validator](pydantic/field_validator.md) |
| Валидатор без `return value` | `l06_practice` | [field_validator](pydantic/field_validator.md) |
| `basicConfig(INFO)` не включает лог SQLAlchemy | `l06_practice`, `l04_orm_basics` | [create_engine](sqlalchemy/create_engine.md) |
| Наивный `datetime.now()` против даты с поясом | `l06_practice`, `p06_pydantic_tasks` | [field_validator](pydantic/field_validator.md) |
| Обработчик с телом `pass` — маршрут отдаёт 500 | `p03_rest_api_classwork` | [Response](flask/Response.md) |
| Импорт по старому имени каталога после переименования | `p02_pydantic_classwork` | [BaseModel](pydantic/BaseModel.md) |
| Обращение к полям объекта после `delete` + `commit` | `l09_orm_practice` | [session.commit](sqlalchemy/session_commit.md) |
| Проверка результата стояла вне `if` и работала по `None` | `l09_orm_practice` | [first / one / all](sqlalchemy/first_one_all.md) |
| Опечатка в имени поля модели (`patern_name`) | `p06_pydantic_tasks` | [Field](pydantic/Field.md) |
| `limit` без `order_by` — «первые N» не те | — | [limit / offset](sqlalchemy/limit_offset.md) |
| Фильтр по оконной функции в `WHERE` | — | [over](sqlalchemy/over.md) |
| Массовый `delete()` не запускает каскады ORM | — | [update / delete](sqlalchemy/bulk_update_delete.md) |
| Каскад по умолчанию не удаляет детей, а ставит FK в `NULL` | — | [session.delete](sqlalchemy/session_delete.md) |
| `lazy='joined'` по коллекции требует `.unique()` | `p09_orm_homework` | [lazy](sqlalchemy/lazy.md) |

Для workflow ошибки другого рода — они ломают запуск в CI, а не код на машине:

| Ошибка | Чем оборачивается | Статья |
|---|---|---|
| `fetch-depth: 1` по умолчанию | нет истории, половина команд git ведёт себя не так | [actions/checkout](github-actions/actions-checkout.md) |
| Нет `permissions: contents: write` | `git push` отдаёт 403, похоже на проблему с паролем | [permissions](github-actions/permissions.md) |
| `${{ inputs.x }}` прямо в тексте `run` | инъекция команд в shell | [выражения](github-actions/expressions.md) |
| `--force` вместо `--force-with-lease` | чужие коммиты затираются молча | [--force-with-lease](git/force-with-lease.md) |

## Запускаемые примеры

В каждом каталоге пакета лежит `examples.py` — он выполняется и печатает результат,
включая исключения из раздела «Частые ошибки». Ловушки показаны не описанием, а настоящим
выводом интерпретатора.

```
cd info/dotenv     && python examples.py
cd info/flask      && python examples.py     # без сервера, через app.test_client()
cd info/pydantic   && python examples.py
cd info/sqlalchemy && python examples.py     # база в памяти, на диске ничего не создаётся
cd info/git        && bash examples.sh       # три временных репозитория, настоящие команды git
```

Ни один пример не занимает порт, не пишет файлы в репозиторий и не требует `.env`.
У `github-actions/` своего `examples.py` нет: workflow выполняется на стороне GitHub,
локально его не запустить. Вместо этого каждая статья ссылается на конкретные строки
реального файла `.github/workflows/main.yml`, а практическая часть вынесена в
[git/copy-repo-to-branch.md](git/copy-repo-to-branch.md) — там всё запускается.

## Проверка ссылок на код

Справочник ссылается на конкретные строки уроков. Код правят — ссылки устаревают,
и документация начинает врать. Чтобы этого не случилось незаметно:

```
cd info
python check_refs.py
```

Скрипт открывает каждый файл по ссылке, берёт указанную строку и сравнивает её с тем,
что процитировано в статье. Возвращает `0`, если всё совпало, и `1` со списком расхождений,
если код уехал вперёд документации.

## Как этим пользоваться

* **Не помню параметр** — открыть статью символа, посмотреть таблицу параметров.
* **Не понимаю код урока** — в `README.md` пакета есть карта «символ → где в коде уроков».
* **Что-то падает** — сначала в раздел «Частые ошибки» нужной статьи: скорее всего,
  эта ошибка там уже разобрана с точным текстом исключения.
* **Хочу попробовать** — `examples.py` рядом, он запускается и ничего не ломает.
