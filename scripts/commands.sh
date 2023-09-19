#!/bin/sh

# ^^^^ tem que ser colocadao para que o docker tente executar o arquivo com esse caminho
# dentro do linux 

# o shell irá encerrar a execução do script quando um comando falhar
set -e

# comando que faz com que o shell espere até que o pastgres esteja ativo e funcionando
# para continuar a execução 
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  echo "🟡 Waiting for Postgres Database Startup ($POSTGRES_HOST $POSTGRES_PORT) ..."
  sleep 2
done

echo "✅ Postgres Database Started Successfully ($POSTGRES_HOST:$POSTGRES_PORT)"

python manage.py collectstatic --noinput
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py runserver 0.0.0.0:8000