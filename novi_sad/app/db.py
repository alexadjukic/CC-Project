from psycopg_pool import ConnectionPool
import os

# print(f"{os.environ.get("CENTRAL_SERVER_PORT", "nema")}")
# print(f"DB_HOST: {os.environ.get("DB_HOST", "NULL")}")
# print(f"PGPORT: {os.environ.get("PGPORT", "NULL")}")
# print(f"POSTGRES_USER: {os.environ.get("POSTGRES_USER", "NULL")}")
# print(f"POSTGRES_PASSWORD: {os.environ.get("POSTGRES_PASSWORD", "NULL")}")

pool = ConnectionPool(
    f"host={os.environ.get("DB_HOST", "localhost")} port={os.environ.get("PGPORT", "5432")} dbname={os.environ.get("POSTGRES_USER", "postgres")} user={os.environ.get("POSTGRES_USER", "postgres")} password={os.environ.get("POSTGRES_PASSWORD", "")}"
)
