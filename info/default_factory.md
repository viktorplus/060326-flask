## Обычное значение по умолчанию

```python
class User(BaseModel):
    is_active: bool = True
```

Значение уже существует и используется, если клиент ничего не передал.

## Динамическое значение

```python
id: UUID = Field(default_factory=uuid4)
```

`default_factory` получает функцию. Pydantic вызывает её при создании каждого нового объекта.