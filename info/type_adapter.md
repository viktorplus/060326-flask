from pydantic import BaseModel, TypeAdapter

class Employee(BaseModel):
    name: str
    age: int

adapter = TypeAdapter(list[Employee])

data = [
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 25}
]

employees = adapter.validate_python(data)


**********************


Employee.model_validate(...)      → один объект

TypeAdapter(list[Employee])       → список объектов

TypeAdapter = проверка сложного типа, например list[Employee].