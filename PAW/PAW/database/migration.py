# migration.py
from database import db

class Migration:
    def __init__(self):
        pass

    def migrate_table(self, table_name, from_version, to_version, migration_query):
        for version in range(from_version + 1, to_version + 1):
            migration_method = getattr(self, f'migrate_{table_name}_to_version_{version}', None)
            if migration_method:
                migration_method(table_name)
                db.set_schema_version(table_name, version)
            else:
                with db.conn:
                    db.conn.execute(migration_query)

# This instance will be used for migrations
migration = Migration()
