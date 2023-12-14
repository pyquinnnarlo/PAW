# migrate_generator.py
from PAW.auth import Auth
import sqlite3

def generate_migration_script():
    connection = sqlite3.connect(':memory:')  # Use an appropriate database connection here
    db = Auth(connection)
    
    cursor = db.conn.execute("PRAGMA table_info(posts)")
    columns = {col[1]: col[2] for col in cursor.fetchall()}
    
    with open("migrate.py", "w") as migrate_file:
        migrate_file.write("# migrate.py\n")
        migrate_file.write("from model import Auth\n\n")
        migrate_file.write("def main():\n")
        migrate_file.write("    connection = sqlite3.connect(':memory:')  # Use an appropriate database connection here\n")
        migrate_file.write("    db = Auth(connection)\n")
        migrate_file.write("    migrations = {\n")
        
        for column, data_type in columns.items():
            migrate_file.write(f"        '{column}': '{data_type}',\n")
        
        migrate_file.write("    }\n")
        migrate_file.write("\n")
        migrate_file.write("    print('Applying migrations...')\n")
        migrate_file.write("    db.apply_migrations(migrations)\n")
        migrate_file.write("    print('Migrations applied successfully.')\n\n")
        migrate_file.write("if __name__ == '__main__':\n")
        migrate_file.write("    main()\n")

if __name__ == "__main__":
    generate_migration_script()
