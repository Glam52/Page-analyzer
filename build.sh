#!/usr/bin/env bash

# Установите переменную DATABASE_URL непосредственно в скрипте
DATABASE_URL="postgresql://postgres:postgres@localhost:5432/hexlet"

# Выполните команды, используя эту переменную
make install && psql -a -d "$DATABASE_URL" -f database.sql
