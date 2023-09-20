#!/bin/sh

# ^^^^ tem que ser colocadao para que o docker tente executar o arquivo com esse caminho
# dentro do linux 

# o shell irá encerrar a execução do script quando um comando falhar
set -e

wait_psql.sh
collectstatic.sh
migrate.sh
runserver.sh