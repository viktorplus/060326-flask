from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from models import User, Address, Base
from sqlalchemy import func

engine = create_engine("sqlite:///practicum3.db")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

with Session() as session:
    # Напишите запрос, который возвращает пользователя с конкретным именем (например, "Alice")
    query = select(User).where(User.name == "Alice")
    user = session.scalar(query)

    print(f"User: {user.id}, {user.name}, age: {user.age}")


    print("*" * 25)
    # Напишите запрос для вывода всех пользователей, возраст которых больше 20 лет.
    query = select(User).where(User.age > 20)
    users = session.scalars(query).all()
    print("Users older than 20:")
    for user in users:
        print(f"User: {user.id}, {user.name}, age: {user.age}")


    # Допустим, вы хотите обновить возраст пользователя "Bob" до 25 лет.
    # Напишите запрос для обновления данных.
    print("*" * 25)
    query = select(User).where(User.name == "Bob")
    user_to_update = session.scalar(query)
    if user_to_update:
        user_to_update.age = 21
        # session.add(user_to_update)
        session.commit()
        print(f"Updated Bob's age to {user_to_update.age}")


    # Пользователи моложе 30 лет
    print("*" * 25)
    query = select(User).where(User.age < 30)
    users = session.scalars(query).all()

    print("Users younger than 30:")
    for user in users:
        print(f"User: {user.id}, {user.name}, age: {user.age}")

    # Напишите запрос, который добавляет пользователя с именем "Charlie".\

    newuser = User (name="Charlie", age=22)
    session.add(newuser)
    session.commit()

    # Удалить Charlie

    user_name="Charlie"
    query = select(User).where(User.name == user_name)
    user_to_delete = session.scalar(query)
    if user_to_delete:
        session.delete(user_to_delete)
        session.commit()
        print(f"Deleted user: {user_name}, id: {user_to_delete}")
    else:
        print(f"User {user_name} not found for deletion.")

    # проверка удаления

    deleted_user = session.get(User, user_to_delete.id)
    if deleted_user:
        print("Не удален")
    else:
        print("Удален")

    # Создайте запрос, который выводит всех пользователей, отсортированных по возрасту
    # в порядке убывания.

    print("*" * 25)
    query = select(User).order_by(User.age.desc())
    users = session.scalars(query).all()
    print("Users sorted by age (descending):")
    for user in users:
        print(f"User: {user.id}, {user.name}, age: {user.age}")

    # Вывод пользователей с ограничением количества:
    query = select(User).limit(3)
    users = session.scalars(query).all()
    print("First 3 users:")
    for user in users:
        print(f"User: {user.id}, {user.name}, age: {user.age}")

    # Обновление данных пользователя по ID



    # Напишите запрос, который выводит первые 4 пользователя, отсортированных по имени в
    # алфавитном порядке

    print("*" * 25)
    query = select(User).order_by(User.name).limit(4)
    users = session.scalars(query).all()
    print("First 4 users sorted by name (alphabetical order):")
    for user in users:
        print(f"User: {user.id}, {user.name}, age: {user.age}")


    # Напишите запрос для обновления данных пользователя, используя его id. Предположим, нужно
    # обновить возраст пользователя с id равным 5 до 35 лет.

    print("*" * 25)
    user_id_to_update = 5
    user_to_update = session.get(User, user_id_to_update)
    if user_to_update:
        user_to_update.age = 35
        session.commit()
        print(f"Updated user with id {user_id_to_update} to age {user_to_update.age}")
    else:
        print(f"User with id {user_id_to_update} not found for update.")


    # Напишите запрос, который проверяет, существует ли пользователь с заданным name.
    # Проверьте наличие пользователя с name равным "Charlie".

    print("*" * 25)
    user_name_to_check = "Charlie"
    query = select(User).where(User.name == user_name_to_check)
    user_exists = session.scalar(query) is not None
    if user_exists:
        print(f"User with name '{user_name_to_check}' exists.")
    else:
        print(f"User with name '{user_name_to_check}' does not exist.")

    # Напишите запрос, который находит средний возраст всех пользователей, и выведите результат.
    print("*" * 25)
    query = select(func.avg(User.age))
    average_age = session.scalar(query)
    print(f"Average age of all users: {average_age:.2f}")


