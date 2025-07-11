from psycopg_pool import ConnectionPool
from dotenv import load_dotenv
import os

load_dotenv()
print(f"DB_HOST: {os.environ.get("DB_HOST", "NULL")}")
print(f"PGPORT: {os.environ.get("PGPORT", "NULL")}")
print(f"POSTGRES_USER: {os.environ.get("POSTGRES_USER", "NULL")}")
print(f"POSTGRES_PASSWORD: {os.environ.get("POSTGRES_PASSWORD", "NULL")}")

pool = ConnectionPool(
    f"host={os.environ.get("DB_HOST", "localhost")} port={os.environ.get("PGPORT", "5432")} dbname={os.environ.get("POSTGRES_USER", "postgres")} user={os.environ.get("POSTGRES_USER", "postgres")} password={os.environ.get("POSTGRES_PASSWORD", "")}"
)

with pool.connection() as conn:
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS users")

    cur.execute(
        """CREATE TABLE users (
	jmbg varchar(13) PRIMARY KEY CHECK (jmbg ~ '^[[:digit:]]{13}$'),
	name varchar(50) NOT NULL,
	surname varchar(50) NOT NULL,
	address varchar(150) NOT NULL
)"""
    )

    cur.executemany(
        "INSERT INTO public.users(jmbg, name, surname, address) VALUES (%s, %s, %s, %s);",
        [
            (
                "1234567890123",
                "Marko",
                "Markovic",
                "adresa 1",
            ),
            (
                "1234567890124",
                "Nikola",
                "Nikolic",
                "adresa 2",
            ),
        ],
    )

    conn.commit()
