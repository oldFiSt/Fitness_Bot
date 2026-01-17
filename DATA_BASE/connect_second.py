import psycopg2
from psycopg2.extras import DictCursor
import config


class DataBase:
    def __init__(self):
        self.conn = psycopg2.connect(
            database="postgres",
            user="postgres",
            password=config.DB_PASSWORD,
            host = "127.0.0.1",
            port = "5432",
        )
        self.cursor = self.conn.cursor(cursor_factory=DictCursor)
        self.create_table()

    def create_table(self):
        my_table = """
        CREATE TABLE IF NOT EXISTS users_info (
            id SERIAL PRIMARY KEY,
            telegram_id BIGINT UNIQUE,
            username VARCHAR(100),
            full_name VARCHAR(100),
            height INTEGER,
            weight DECIMAL(5,2),
            age INTEGER,
            gender VARCHAR(10),
            goal VARCHAR(20),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            points INTEGER DEFAULT 0
        );
        """
        self.cursor.execute(my_table)
        self.conn.commit()

    def add_user(self, telegram_id, username, full_name, height, weight, age, gender, goal, created_at=None):
        sql = """
              INSERT INTO users_info (telegram_id, username, full_name, height, weight, age, gender, goal, created_at)
              VALUES (%s, %s, %s, %s, %s, %s, %s, %s, COALESCE(%s, CURRENT_TIMESTAMP)) ON CONFLICT (telegram_id)
        DO \
              UPDATE SET
                  username = EXCLUDED.username, \
                  full_name = EXCLUDED.full_name, \
                  height = EXCLUDED.height, \
                  weight = EXCLUDED.weight, \
                  age = EXCLUDED.age, \
                  gender = EXCLUDED.gender, \
                  goal = EXCLUDED.goal; \
              """
        self.cursor.execute(sql, (telegram_id, username, full_name, height, weight, age, gender, goal, created_at))
        self.conn.commit()

    def get_user(self, telegram_id):
        sql = "SELECT * FROM users_info WHERE telegram_id = %s"
        self.cursor.execute(sql, (telegram_id,))
        return self.cursor.fetchone()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def upsert_user(self, telegram_id: int, full_name: str, username: str | None = None):
        sql = """
              INSERT INTO users_info (telegram_id, username, full_name)
              VALUES (%s, %s, %s) ON CONFLICT (telegram_id) DO \
              UPDATE SET
                  username = EXCLUDED.username, \
                  full_name = EXCLUDED.full_name; \
              """
        self.cursor.execute(sql, (telegram_id, username, full_name))
        self.conn.commit()

    def add_points(self, telegram_id: int, points: int):
        sql = "UPDATE users_info SET points = COALESCE(points,0) + %s WHERE telegram_id = %s;"
        self.cursor.execute(sql, (points, telegram_id))
        self.conn.commit()

    def get_top(self, limit: int = 10):
        sql = """
              SELECT telegram_id, full_name, points
              FROM users_info
              ORDER BY points DESC NULLS LAST, telegram_id ASC
                  LIMIT %s; \
              """
        self.cursor.execute(sql, (limit,))
        return self.cursor.fetchall()

    def get_rank(self, telegram_id: int):
        sql = """
              SELECT 1 + COUNT(*)
              FROM users_info
              WHERE COALESCE(points, 0) > (SELECT COALESCE(points, 0) \
                                           FROM users_info \
                                           WHERE telegram_id = %s); \
              """
        self.cursor.execute(sql, (telegram_id,))
        row = self.cursor.fetchone()
        return row[0] if row else None


db = DataBase()
