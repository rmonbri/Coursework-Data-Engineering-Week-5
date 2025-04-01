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