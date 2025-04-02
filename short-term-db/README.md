# Short term DB

Data stored in the short-term DB (readings < 24h old) 
Files here should be relevant to this db including:

- Schema
- Terraform files
- Any  utils to clear / reformat the db
- Following chanes / migrations?

---

## Schema

ERD Diagram can be found [Here](https://drawsql.app/teams/sigma-labs-37/diagrams/lmnh-plants). This is the schema for the short term db and should match it exactly.

The command:

`sqlcmd -S <host> -U <user> -P <password> -i schema.sql`

Will run the schema.

The database does not need to be specified in the command but a database called `lmnh_plants` should exist.


The Schema file will create tables under the default `dbo` schema. This is fine for our application.

---

### Utilities

- Some tools/scripts for making frequent database operations easier have been provided.
- They **REQUIRE** `sqlcmd` to be installed it can be installed via brew with `brew install sqlcmd`
- They also require a .env with variables:

```
DB_USERNAME=
DB_PASSWORD=
DB_HOST=
```


`clear_measurements.sh` / `clear_measurements.sql` clear the `measurement` table in the database. Either can be executed (the bash file calls the sql file). The bash file requires a `.env` with variables:

`reset_db.sh` is a simpler way of running the `schema.sql` on the DB to reset it manually.
