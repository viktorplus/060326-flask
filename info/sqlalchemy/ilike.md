# .ilike() / .like()

```python
select(User).where(User.username.ilike('U%'))
```

**Что это.** Поиск по шаблону. `like` учитывает регистр, `ilike` — нет.

**Зачем.** Поиск «начинается с», «содержит» — самая частая задача в фильтрах интерфейса.

## Сигнатура

```python
колонка.like(pattern)      # с учётом регистра
колонка.ilike(pattern)     # без учёта регистра
колонка.startswith(s)  .endswith(s)  .contains(s)
```

## Параметры

| Параметр | Тип | По умолчанию | Что делает |
|---|---|---|---|
| ``%`` | — | — | Любое количество любых символов |
| ``_`` | — | — | Ровно один любой символ |

## Минимальный пример

```python
select(User).where(User.username.ilike('U%'))      # начинается на U или u
select(User).where(User.username.ilike('%admin%')) # содержит admin
select(User).where(User.username.like('U%'))       # ровно заглавная U
```

## Типичные задачи

**Безопаснее без ручных процентов**

```python
select(User).where(User.username.startswith('user'))
select(User).where(User.username.contains('adm'))
```

**Экранировать проценты в пользовательском вводе**

```python
term = user_input.replace('%', r'\%').replace('_', r'\_')
select(User).where(User.username.ilike(f'%{term}%', escape='\\'))
```

## Частые ошибки

- **SQLite и `like` для не-ASCII.** Встроенный `LIKE` там не учитывает регистр только для латиницы: `ilike('П%')` и `like('п%')` могут вести себя неожиданно с кириллицей.
- **`%` внутри пользовательского ввода** превращает поиск в «что угодно». Экранируйте.
- **Шаблон, начинающийся с `%`,** не может использовать индекс — на большой таблице это медленно.

## Где в репозитории

- `l05_orm_relationships/app.py:227` — `query = select(User).where(User.username.ilike('U%'))`
- `l05_orm_relationships/app.py:246` — `query = select(User).where(or_(User.username.ilike('U%'), User.username.ilike('A%')))`

## См. также

[where](where.md), [in_](in_.md), [between](between.md)
