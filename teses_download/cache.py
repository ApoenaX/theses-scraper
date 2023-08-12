import os
import sqlite3
from abc import ABC, abstractmethod
from threading import Lock
from functools import lru_cache


class __AbstractCache(ABC):
    def __init__(self, path: str):
        self.path = path

    @abstractmethod
    def __getitem__(self, key: str):
        """Get value from cache.

        Args:
            key (str): Key to get value from cache.
        """
        pass

    @abstractmethod
    def __setitem__(self, key: str, value: str):
        """Set value to cache.

        Args:
            key (str): Key to set value to cache.
            value (str): Value to set to cache.
        """
        pass

    @abstractmethod
    def __delitem__(self, key: str):
        """Delete value from cache.

        Args:
            key (str): Key to delete value from cache.
        """
        pass

    @abstractmethod
    def __contains__(self, key: str):
        """Check if key is in cache.

        Args:
            key (str): Key to check if is in cache.
        """
        pass


class Cache(__AbstractCache):
    def __init__(self, path: str, db_name: str = "cache.sqlite3"):
        super(Cache, self).__init__(path)
        os.makedirs(path, exist_ok=True)
        self.path = path
        self.db_name = os.path.join(path, db_name)
        self.lock = Lock()
        self._init_db()

    def _init_db(self):
        with self.lock:
            with sqlite3.connect(self.db_name) as conn:
                conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS cache (
                        key TEXT PRIMARY KEY,
                        value TEXT
                    )
                    """
                )

    def __str__(self):
        return f"Cache(path={self.path}, db_name={self.db_name})"

    def __len__(self):
        with self.lock:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.execute(
                    """
                    SELECT COUNT(*) FROM cache
                    """
                )
                return cursor.fetchone()[0]

    def __iter__(self):
        return iter(self.keys())

    def __reversed__(self):
        return reversed(self.keys())

    @lru_cache(maxsize=1)
    def __getitem__(self, key: str):
        with self.lock:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.execute(
                    """
                    SELECT value FROM cache WHERE key = ?
                    """,
                    (key,),
                )
                result = cursor.fetchone()
                if result:
                    return result[0]
                return None

    def __setitem__(self, key: str, value: str):
        with self.lock:
            with sqlite3.connect(self.db_name) as conn:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO cache (key, value) VALUES (?, ?)
                    """,
                    (key, value),
                )
            self.__getitem__.cache_clear()

    def __delitem__(self, key: str):
        with self.lock:
            with sqlite3.connect(self.db_name) as conn:
                conn.execute(
                    """
                    DELETE FROM cache WHERE key = ?
                    """,
                    (key,),
                )
            self.__getitem__.cache_clear()

    def __contains__(self, key: str):
        with self.lock:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.execute(
                    """
                    SELECT value FROM cache WHERE key = ?
                    """,
                    (key,),
                )
                result = cursor.fetchone()
                return result is not None

    def clear(self):
        with self.lock:
            with sqlite3.connect(self.db_name) as conn:
                conn.execute(
                    """
                    DELETE FROM cache
                    """
                )
            self.__getitem__.cache_clear()

    def get(self, key: str, default: str = None):
        return self[key] or default

    def set(self, key: str, value: str):
        self[key] = value

    def keys(self):
        with self.lock:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.execute(
                    """
                    SELECT key FROM cache
                    """
                )
                return [i[0] for i in cursor.fetchall()]

    def values(self):
        with self.lock:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.execute(
                    """
                    SELECT value FROM cache
                    """
                )
                return [i[0] for i in cursor.fetchall()]

    def items(self):
        with self.lock:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.execute(
                    """
                    SELECT key, value FROM cache
                    """
                )
                return [(i[0], i[1]) for i in cursor.fetchall()]


def create_cache(path: str, db_name: str = "cache.db") -> Cache:
    return Cache(path, db_name)
