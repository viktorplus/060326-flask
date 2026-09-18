#!/usr/bin/env bash
# Запускаемые примеры к справочнику git.
#
#     cd info/git
#     bash examples.sh
#
# Скрипт поднимает три временных репозитория во временном каталоге и показывает,
# как скопировать репозиторий в отдельную ветку — на настоящих командах git.
# Репозиторий курса не затрагивается вообще: всё происходит в каталоге для
# временных файлов, который удаляется в конце.

set -uo pipefail

title() { printf '\n%s\n%s. %s\n%s\n' "======================================================================" "$1" "$2" "======================================================================"; }
run()   { printf '  $ %s\n' "$*"; "$@" 2>&1 | sed 's/^/    /'; }

TMP="$(mktemp -d 2>/dev/null || mktemp -d -t gitdemo)"
trap 'rm -rf "$TMP"' EXIT

# Общие настройки, чтобы демонстрация не зависела от глобального конфига
export GIT_CONFIG_GLOBAL="$TMP/gitconfig"
export GIT_CONFIG_SYSTEM="$TMP/gitconfig"
git config --global user.email "demo@example.com"
git config --global user.name "Demo"
git config --global init.defaultBranch main

# ---------------------------------------------------------------------------
title 0 "Готовим сцену: чужой репозиторий, наш репозиторий, наша рабочая копия"

# «Репозиторий преподавателя» — тот, откуда копируем
git init -q --bare "$TMP/upstream.git"
git clone -q "$TMP/upstream.git" "$TMP/upstream-work"
(
  cd "$TMP/upstream-work"
  echo "урок 1" > lesson.txt && git add . && git commit -qm "lesson 1"
  echo "урок 2" >> lesson.txt && git add . && git commit -qm "lesson 2"
  git push -q origin main
)

# «Наш репозиторий» на сервере и наша рабочая копия
git init -q --bare "$TMP/origin.git"
git clone -q "$TMP/origin.git" "$TMP/work"
(
  cd "$TMP/work"
  echo "моя работа" > mine.txt && git add . && git commit -qm "my work"
  git push -q -u origin main
)

echo "  upstream.git — репозиторий преподавателя (2 коммита)"
echo "  origin.git   — наш репозиторий (1 коммит)"
echo "  work/        — наша рабочая копия"

cd "$TMP/work"

# ---------------------------------------------------------------------------
title 1 "git remote: объявляем чужой репозиторий"

run git remote add upstream "$TMP/upstream.git"
run git remote -v

echo
echo "  Повторный add падает — поэтому в скриптах пишут 'add || set-url':"
run git remote add upstream "$TMP/upstream.git"
echo "  (код возврата выше ненулевой, и именно на это рассчитана идиома с ||)"

# ---------------------------------------------------------------------------
title 2 "git fetch: скачиваем, НЕ меняя свои ветки"

echo "  до fetch — наши ветки:"
run git branch -a

run git fetch upstream main

echo "  после fetch появилась ссылка upstream/main, но локальных веток не прибавилось:"
run git branch -a
echo
echo "  рабочие файлы тоже не тронуты:"
run ls

# ---------------------------------------------------------------------------
title 3 "ГЛАВНОЕ: push с refspec кладёт чужую ветку в нашу — без переключения"

BRANCH="teacher/2026-09-18"
echo "  Слева от двоеточия — ОТКУДА берём, справа — КУДА кладём."
run git push origin "upstream/main:refs/heads/$BRANCH"

echo
echo "  Наша текущая ветка не изменилась:"
run git branch --show-current
echo "  Рабочие файлы не изменились:"
run ls

# ---------------------------------------------------------------------------
title 4 "git ls-remote: проверяем результат, ничего не скачивая"

run git ls-remote --heads origin
echo
echo "  Вывод — две колонки через табуляцию: SHA и полное имя ссылки."
REMOTE_SHA="$(git ls-remote --heads origin "refs/heads/$BRANCH" | awk 'NR == 1 { print $1 }')"
echo "  SHA ветки $BRANCH: $REMOTE_SHA"

echo
echo "  Несуществующая ветка — пустой вывод и код возврата 0, а НЕ ошибка:"
MISSING="$(git ls-remote --heads origin "refs/heads/нет-такой" | awk 'NR == 1 { print $1 }')"
echo "    результат: '$MISSING'  (код возврата: $?)"
echo "    поэтому в скриптах проверяют непустоту: [ -n \"\$X\" ]"

# ---------------------------------------------------------------------------
title 5 "git check-ref-format: проверка имени до того, как оно попадёт в git"

for name in "teacher/2026-09-18" "с пробелом" "две..точки" "плохое~имя"; do
  if git check-ref-format --branch "$name" >/dev/null 2>&1; then
    printf '    %-22s -> годится\n' "$name"
  else
    printf '    %-22s -> ОТКЛОНЕНО\n' "$name"
  fi
done
echo
echo "  Команда молчит при успехе и сообщает результат только кодом возврата —"
echo "  поэтому её ставят под set -e."

# ---------------------------------------------------------------------------
title 6 "Обновление снимка: --force-with-lease защищает от чужих правок"

# Преподаватель добавил урок 3
(
  cd "$TMP/upstream-work"
  echo "урок 3" >> lesson.txt && git add . && git commit -qm "lesson 3"
  git push -q origin main
)
run git fetch upstream main

echo
echo "  Случай А: ветку никто не трогал — перезапись проходит."
run git push --force-with-lease="refs/heads/$BRANCH:$REMOTE_SHA" origin "upstream/main:refs/heads/$BRANCH"

echo
echo "  Случай Б: кто-то изменил ветку, а мы этого не знаем."
# Посторонний делает СВОЙ коммит и кладёт его в ту же ветку
(
  cd "$TMP/upstream-work"
  git checkout -q -b intruder
  echo "правка постороннего" >> lesson.txt
  git add . && git commit -qm "outsider change"
  git push -q "$TMP/origin.git" "intruder:refs/heads/$BRANCH" --force
)
NOW_SHA="$(git ls-remote --heads origin "refs/heads/$BRANCH" | awk 'NR == 1 { print $1 }')"
echo "  (посторонний перезаписал $BRANCH, теперь она на $NOW_SHA)"
echo "  Мы же всё ещё считаем, что она на $REMOTE_SHA:"
run git push --force-with-lease="refs/heads/$BRANCH:$REMOTE_SHA" origin "upstream/main:refs/heads/$BRANCH"
echo "  -> push ОТКЛОНЁН. Это не поломка, а сработавшая защита:"
echo "     --force просто затёр бы чужие изменения молча."

# ---------------------------------------------------------------------------
title 7 "Другие способы сделать копию"

echo "  Локальная ветка из чужой — создать, НЕ переключаясь:"
run git branch snapshot-local upstream/main
run git branch -vv

echo
echo "  Копия ТЕКУЩЕГО состояния в запасную ветку, одной командой:"
run git push origin "HEAD:refs/heads/backup-demo"

echo
echo "  Ветка из конкретного коммита:"
FIRST="$(git rev-list --max-parents=0 upstream/main | tail -1)"
run git push origin "$FIRST:refs/heads/from-first-commit"

echo
echo "  Итог на сервере:"
run git ls-remote --heads origin

# ---------------------------------------------------------------------------
title 8 "Истории не связаны — слить снимок с нашей веткой просто так нельзя"

run git merge snapshot-local
echo "  -> 'refusing to merge unrelated histories' — это ожидаемо."
echo "     У чужого репозитория своя история. Нужен --allow-unrelated-histories,"
echo "     и конфликты придётся разбирать руками."

# ---------------------------------------------------------------------------
title 9 "Удаление ветки на сервере"

run git push origin --delete from-first-commit
echo "  То же самое через refspec с пустым источником (двоеточие в начале):"
run git push origin ":refs/heads/backup-demo"
run git ls-remote --heads origin

printf '\nГотово. Все репозитории были временными и сейчас удалены.\n'
printf 'Репозиторий курса не затронут.\n'
