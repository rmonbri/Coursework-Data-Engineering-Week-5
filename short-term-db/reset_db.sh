source .env

echo "Running..."
sqlcmd -S $DB_HOST -U $DB_USERNAME -P $DB_PASSWORD -i schema.sql