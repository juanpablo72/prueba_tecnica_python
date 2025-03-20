#!/bin/sh

# Esperar a que PostgreSQL esté listo
until python manage.py check --database default; do
  echo "PostgreSQL no está disponible aún. Esperando..."
  sleep 2
done

# Ejecutar migraciones y comandos necesarios
python manage.py migrate
python manage.py collectstatic --no-input

exec "$@"