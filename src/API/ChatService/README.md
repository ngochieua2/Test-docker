--setup  lib
--Stand for "ChatService" run "pip install -r requirements.txt"

--start project
--"ChatService" dic: uvicorn app.main:app --reload

--migration
--migration-add: alembic revision --autogenerate -m "<migration name>"

--upgrade to latest version
--migration-upgrade: alembic upgrade head

--Replace <revision_id> with the hash shown in alembic history.
--migration-downgrade: alembic downgrade <revision_id>

--This rolls back the latest migration.
--migration-downgrade (latest): alembic downgrade -1

--This reverts all migrations (removes all tables).
--migration-downgrade (base): alembic downgrade base