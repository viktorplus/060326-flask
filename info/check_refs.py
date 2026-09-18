# -*- coding: utf-8 -*-
"""Проверяет, что ссылки справочника на код уроков не разошлись с реальностью.

    cd info
    python check_refs.py

Каждая статья в разделе «Где в репозитории» содержит строки вида

    - `l05_orm_relationships/app.py:179` *(пометка)* — `текст строки кода`

Скрипт открывает указанный файл, берёт указанную строку и сравнивает её с
процитированным текстом. Расхождение означает, что код правили, а справочник —
нет: ссылка теперь показывает не на то место.

Код возврата: 0 — все ссылки целы, 1 — есть расхождения.
"""
from __future__ import annotations

import pathlib
import re
import sys

INFO = pathlib.Path(__file__).resolve().parent
ROOT = INFO.parent

# - `путь:строка` *(необязательная пометка)* — `процитированный код`
REF = re.compile(r"^- `([^`:]+):(\d+)`(?: \*\([^)]*\)\*)? — `(.*)`$")

# Ссылки из статей режутся по длине при генерации — сравниваем по началу строки
TRUNCATED_AT = 100


def main() -> int:
    articles = sorted(p for p in INFO.rglob("*.md") if p.name != "README.md")
    articles += sorted(INFO.glob("*/README.md"))

    total = ok = 0
    problems: list[str] = []
    cache: dict[pathlib.Path, list[str]] = {}

    for article in articles:
        for lineno, raw in enumerate(article.read_text(encoding="utf-8").splitlines(), 1):
            m = REF.match(raw.strip())
            if not m:
                continue
            rel, num, quoted = m.group(1), int(m.group(2)), m.group(3)
            total += 1
            where = f"{article.relative_to(ROOT).as_posix()}:{lineno}"

            target = ROOT / rel
            if not target.exists():
                problems.append(f"{where}\n    файла нет: {rel}")
                continue

            if target not in cache:
                cache[target] = target.read_text(encoding="utf-8").splitlines()
            lines = cache[target]

            if num > len(lines):
                problems.append(
                    f"{where}\n    в файле {rel} всего {len(lines)} строк, а ссылка на {num}")
                continue

            actual = lines[num - 1].strip()[:TRUNCATED_AT]
            if actual != quoted:
                problems.append(
                    f"{where}\n    ссылка:   {rel}:{num}\n"
                    f"    ожидалось: {quoted}\n"
                    f"    на месте:  {actual}")
                continue
            ok += 1

    print(f"Проверено ссылок: {total}")
    print(f"Совпало:          {ok}")
    print(f"Расхождений:      {len(problems)}")

    if problems:
        print("\nРасхождения (код правили, справочник — нет):")
        for p in problems:
            print("\n  " + p.replace("\n", "\n  "))
        print("\nПочинить: перегенерировать статьи либо поправить номера строк вручную.")
        return 1

    print("\nВсе ссылки ведут на то место в коде, которое процитировано.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
