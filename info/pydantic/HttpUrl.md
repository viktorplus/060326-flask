# HttpUrl

```python
from pydantic import HttpUrl
```

**Что это.** Тип-валидатор: строка, которая обязана быть корректной ссылкой `http://` или `https://`.

**Зачем.** То же, что с почтой: разбирать URL руками долго и ненадёжно. Заодно значение приходит уже разобранным на части — схему, хост, путь.

## Сигнатура

```python
url: HttpUrl
```

## Минимальный пример

```python
from pydantic import BaseModel, HttpUrl

class Product(BaseModel):
    url: HttpUrl

p = Product(url='https://example.com/item?id=1')
print(p.url.host, p.url.scheme)
```

Вывод:

```
example.com https
```

## Частые ошибки

- **Ожидать обычную строку.** `HttpUrl` — отдельный тип. Чтобы получить строку, используйте `str(p.url)`; при `model_dump(mode='json')` это происходит само.
- **`AnyUrl` против `HttpUrl`.** `AnyUrl` пропустит `ftp://` и другие схемы; `HttpUrl` — только http и https.

## Где в репозитории

- `l02_pydantic_models/models.py:13` — `from pydantic import BaseModel, EmailStr, ValidationError, Field, HttpUrl, field_validator, ConfigDi`
- `l02_pydantic_models/models.py:43` — `url: HttpUrl`
- `l02_pydantic_models/models.py:10` *(в закомментированном учебном блоке)* — `# HttpUrl        — тип-валидатор http/https-ссылки.`
- `l02_pydantic_models/models.py:42` *(в закомментированном учебном блоке)* — `# HttpUrl отвергнет строку, которая не является корректным http(s)-адресом.`

## См. также

[EmailStr](EmailStr.md), [Field](Field.md)
