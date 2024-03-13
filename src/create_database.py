import sqlite3
import os
import sys
from config import Config


def create_sqlite_db(folder_path):
    os.makedirs(folder_path, exist_ok=True)

    database_file = os.path.join(folder_path, Config.DB)

    conn = sqlite3.connect(database_file)
    print(f"Database '{database_file}' created successfully!")
    conn.close()


if __name__ == "__main__":
    folder_path = sys.argv[1]
    create_sqlite_db(folder_path)
