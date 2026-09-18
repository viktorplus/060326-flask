# -*- coding: utf-8 -*-
"""Запускаемые примеры к справочнику python-dotenv.

    cd info/dotenv
    python examples.py

Скрипт самодостаточен: создаёт временный .env во временном каталоге,
показывает поведение и убирает за собой. Настоящий .env репозитория не трогает.
"""
import os
import tempfile
from pathlib import Path

from dotenv import load_dotenv, dotenv_values, find_dotenv, set_key


def title(n: int, text: str) -> None:
    print(f"\n{'=' * 70}\n{n}. {text}\n{'=' * 70}")


tmp = Path(tempfile.mkdtemp(prefix="dotenv_demo_"))
env_file = tmp / ".env"
env_file.write_text(
    "DB_USERNAME=admin\n"
    "DRIVER=sqlite\n"
    "PORT=5000\n"
    "DEBUG=0\n"
    "EMPTY=\n"
    "GREETING=Привет, ${DB_USERNAME}\n",
    encoding="utf-8",
)

# ---------------------------------------------------------------------------
title(1, "dotenv_values — прочитать файл, не трогая окружение")

values = dotenv_values(env_file)
print("словарь из файла:", dict(values))
print("а в os.environ ключа нет:", "PORT" in os.environ)

# ---------------------------------------------------------------------------
title(2, "load_dotenv — перенести значения в os.environ")

load_dotenv(env_file)
print("DB_USERNAME =", os.environ.get("DB_USERNAME"))
print("DRIVER      =", os.environ.get("DRIVER"))

# ---------------------------------------------------------------------------
title(3, "ГЛАВНАЯ ЛОВУШКА: override=False не перезапишет существующую переменную")

os.environ["DRIVER"] = "уже-было-в-окружении"
load_dotenv(env_file)                       # override=False по умолчанию
print("после load_dotenv():          ", os.environ["DRIVER"])
print("значение из файла при этом:   ", dotenv_values(env_file)["DRIVER"])
print("-> файл прочитан, но значение отброшено, и никакой ошибки не было")

load_dotenv(env_file, override=True)        # а вот так перезапишет
print("после override=True:          ", os.environ["DRIVER"])

# ---------------------------------------------------------------------------
title(4, "Почему ключ называется DB_USERNAME, а не USERNAME")

system_username = os.environ.get("USERNAME")
print("USERNAME в системе:", repr(system_username))
print("-> на Windows это имя пользователя ОС. Положи мы в .env ключ USERNAME,")
print("   при override=False он был бы молча проигнорирован, и приложение")
print("   получило бы имя пользователя Windows вместо значения из файла.")

# ---------------------------------------------------------------------------
title(5, "Все значения — строки, тип приводим сами")

port_raw = os.environ.get("PORT")
debug_raw = os.environ.get("DEBUG")
print(f"PORT  = {port_raw!r} -> int:  {int(port_raw)}")
print(f"DEBUG = {debug_raw!r}")
print(f"  bool({debug_raw!r}) = {bool(debug_raw)}   <- ЛОВУШКА: непустая строка всегда True")
print(f"  правильно: {debug_raw!r} == '1' -> {debug_raw == '1'}")

# ---------------------------------------------------------------------------
title(6, "Пустое значение и подстановка ${...}")

raw = dotenv_values(env_file)
print("EMPTY=   в файле дало:", repr(raw["EMPTY"]), "(пустая строка, не None)")
print("GREETING с подстановкой:", repr(raw["GREETING"]))
no_interp = dotenv_values(env_file, interpolate=False)
print("он же с interpolate=False:", repr(no_interp["GREETING"]))

# ---------------------------------------------------------------------------
title(7, "find_dotenv — найти файл, поднимаясь вверх по дереву")

deep = tmp / "a" / "b" / "c"
deep.mkdir(parents=True, exist_ok=True)
old_cwd = Path.cwd()
try:
    os.chdir(deep)
    found = find_dotenv(usecwd=True)
    print("запущено из:", deep)
    print("найден файл:", found or "(не найден)")
finally:
    os.chdir(old_cwd)

print("\nа если файла нет — вернётся пустая строка, а не исключение:")
empty_dir = Path(tempfile.mkdtemp(prefix="dotenv_empty_"))
try:
    os.chdir(empty_dir)
    print("  find_dotenv() ->", repr(find_dotenv(usecwd=True)))
    print("  load_dotenv('') тихо ничего не делает ->", load_dotenv(""))
finally:
    os.chdir(old_cwd)

# ---------------------------------------------------------------------------
title(8, "set_key — запись из программы")

set_key(str(env_file), "DRIVER", "postgresql")
print("DRIVER в файле стал:", dotenv_values(env_file)["DRIVER"])
print("содержимое файла после записи:")
print("  " + env_file.read_text(encoding="utf-8").replace("\n", "\n  ").rstrip())
print("-> обратите внимание: кавычки расставлены автоматически (quote_mode='always')")

# ---------------------------------------------------------------------------
title(9, "Проверка: шаблон и рабочий файл не разошлись по ключам")

example_file = tmp / ".env.example"
example_file.write_text("DB_USERNAME=\nDRIVER=\nSECRET_KEY=\n", encoding="utf-8")

expected = set(dotenv_values(example_file))
actual = set(dotenv_values(env_file))
missing = expected - actual
print("ключи в .env.example:", sorted(expected))
print("ключи в .env        :", sorted(actual))
print("не хватает          :", sorted(missing) or "нечего добавлять")

# ---------------------------------------------------------------------------
import shutil

shutil.rmtree(tmp, ignore_errors=True)
shutil.rmtree(empty_dir, ignore_errors=True)
print("\nВременные файлы удалены.")
