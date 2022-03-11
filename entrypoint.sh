#!/bin/bash

echo "Apply migrations and basic data creation "

pw_migrate migrate --directory application/migrations --database "postgresql://$DB_LOGIN:$DB_PASSWORD@$DB_HOST/$DB_NAME"

echo "Starting server"
python3 -m runner
