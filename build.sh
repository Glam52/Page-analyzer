#!/usr/bin/env bash

# Установите переменную DATABASE_URL непосредственно в скрипте
DATABASE_URL="postgresql://hexlet_428q_user:URj6a9NJ9Q20qdpKbI0S5eKeddjsxQiq@dpg-crn3ss56l47c73a97rng-a.oregon-postgres.render.com/hexlet_428q"

# Выполните команды, используя эту переменную
make install && psql -a -d "$DATABASE_URL" -f database.sql
