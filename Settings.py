from pathlib import Path

ROOT = Path(__file__).resolve().parent

ENCODING = "UTF-8"

''' DATABASE '''
DATABASE_ENGINE = "sqlite"
DATABASE_PATH = ROOT / "Database.sqlite"
HASH_SALT = "$2b$12$Yvl0y/IrIZUF0vwN6wML/O".encode("UTF-8")

if __name__ == "__main__":
    print(ROOT)