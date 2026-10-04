from contextlib import contextmanager

from pgvector.psycopg import register_vector
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

from app.config import settings

pool: ConnectionPool | None = None


def _configure(conn):
    register_vector(conn)
    conn.commit()


def open_pool() -> None:
    global pool
    if pool is not None:
        return
    pool = ConnectionPool(
        settings.database_url,
        min_size=1,
        max_size=10,
        kwargs={"row_factory": dict_row},
        configure=_configure,
        check=ConnectionPool.check_connection,  # Neon closes idle connections
        open=False,
    )
    pool.open(wait=True, timeout=30)


def close_pool() -> None:
    global pool
    if pool is not None:
        pool.close()
        pool = None


@contextmanager
def get_conn():
    """One connection = one transaction. Commits on success, rolls back on error."""
    if pool is None:
        open_pool()
    with pool.connection() as conn:
        yield conn
