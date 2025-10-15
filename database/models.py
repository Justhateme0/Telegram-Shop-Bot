import aiosqlite
import sqlite3
from datetime import datetime
from typing import Optional, List, Dict, Any

class DatabaseManager:
    def __init__(self, db_path: str = "bot_database.db"):
        self.db_path = db_path

    async def init_db(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    telegram_id INTEGER UNIQUE NOT NULL,
                    username TEXT,
                    first_name TEXT,
                    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            await db.execute('''
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    product_category TEXT NOT NULL,
                    product_name TEXT NOT NULL,
                    price_rub INTEGER,
                    price_usd INTEGER,
                    status TEXT DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    payment_screenshot TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (telegram_id)
                )
            ''')

            await db.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT NOT NULL,
                    name TEXT NOT NULL,
                    price_rub INTEGER,
                    price_usd INTEGER,
                    description TEXT,
                    availability BOOLEAN DEFAULT 1
                )
            ''')

            await db.execute('''
                CREATE TABLE IF NOT EXISTS settings (
                    id INTEGER PRIMARY KEY,
                    usdt_wallet TEXT,
                    admin_id INTEGER
                )
            ''')

            await db.commit()

    async def add_user(self, telegram_id: int, username: str = None, first_name: str = None) -> bool:
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    'INSERT OR IGNORE INTO users (telegram_id, username, first_name) VALUES (?, ?, ?)',
                    (telegram_id, username, first_name)
                )
                await db.commit()
                return True
        except Exception:
            return False

    async def get_user(self, telegram_id: int) -> Optional[Dict[str, Any]]:
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                async with db.execute(
                    'SELECT * FROM users WHERE telegram_id = ?', (telegram_id,)
                ) as cursor:
                    row = await cursor.fetchone()
                    return dict(row) if row else None
        except Exception:
            return None

    async def create_order(
        self,
        user_id: int,
        product_category: str,
        product_name: str,
        price_rub: int = None,
        price_usd: int = None
    ) -> Optional[int]:
        try:
            async with aiosqlite.connect(self.db_path) as db:
                cursor = await db.execute(
                    '''INSERT INTO orders
                    (user_id, product_category, product_name, price_rub, price_usd)
                    VALUES (?, ?, ?, ?, ?)''',
                    (user_id, product_category, product_name, price_rub, price_usd)
                )
                await db.commit()
                return cursor.lastrowid
        except Exception:
            return None

    async def get_order(self, order_id: int) -> Optional[Dict[str, Any]]:
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                async with db.execute(
                    'SELECT * FROM orders WHERE id = ?', (order_id,)
                ) as cursor:
                    row = await cursor.fetchone()
                    return dict(row) if row else None
        except Exception:
            return None

    async def update_order_status(self, order_id: int, status: str) -> bool:
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    'UPDATE orders SET status = ? WHERE id = ?',
                    (status, order_id)
                )
                await db.commit()
                return True
        except Exception:
            return False

    async def add_payment_screenshot(self, order_id: int, file_id: str) -> bool:
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    'UPDATE orders SET payment_screenshot = ?, status = ? WHERE id = ?',
                    (file_id, 'waiting_confirmation', order_id)
                )
                await db.commit()
                return True
        except Exception:
            return False

    async def get_pending_orders(self) -> List[Dict[str, Any]]:
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                async with db.execute(
                    '''SELECT o.*, u.username, u.first_name
                    FROM orders o
                    JOIN users u ON o.user_id = u.telegram_id
                    WHERE o.status = "waiting_confirmation"
                    ORDER BY o.created_at DESC'''
                ) as cursor:
                    rows = await cursor.fetchall()
                    return [dict(row) for row in rows]
        except Exception:
            return []

    async def get_user_orders(self, user_id: int) -> List[Dict[str, Any]]:
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                async with db.execute(
                    'SELECT * FROM orders WHERE user_id = ? ORDER BY created_at DESC',
                    (user_id,)
                ) as cursor:
                    rows = await cursor.fetchall()
                    return [dict(row) for row in rows]
        except Exception:
            return []

    async def get_orders_stats(self) -> Dict[str, int]:
        try:
            async with aiosqlite.connect(self.db_path) as db:
                stats = {}

                async with db.execute('SELECT COUNT(*) FROM orders') as cursor:
                    row = await cursor.fetchone()
                    stats['total'] = row[0] if row else 0

                async with db.execute('SELECT COUNT(*) FROM orders WHERE status = "completed"') as cursor:
                    row = await cursor.fetchone()
                    stats['completed'] = row[0] if row else 0

                async with db.execute('SELECT COUNT(*) FROM orders WHERE status = "pending"') as cursor:
                    row = await cursor.fetchone()
                    stats['pending'] = row[0] if row else 0

                async with db.execute('SELECT COUNT(*) FROM orders WHERE status = "waiting_confirmation"') as cursor:
                    row = await cursor.fetchone()
                    stats['waiting'] = row[0] if row else 0

                return stats
        except Exception:
            return {'total': 0, 'completed': 0, 'pending': 0, 'waiting': 0}

    async def get_users_count(self) -> int:
        try:
            async with aiosqlite.connect(self.db_path) as db:
                async with db.execute('SELECT COUNT(*) FROM users') as cursor:
                    row = await cursor.fetchone()
                    return row[0] if row else 0
        except Exception:
            return 0

    async def get_all_users(self) -> List[int]:
        try:
            async with aiosqlite.connect(self.db_path) as db:
                async with db.execute('SELECT telegram_id FROM users') as cursor:
                    rows = await cursor.fetchall()
                    return [row[0] for row in rows]
        except Exception:
            return []

    async def set_usdt_wallet(self, wallet: str) -> bool:
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    'INSERT OR REPLACE INTO settings (id, usdt_wallet) VALUES (1, ?)',
                    (wallet,)
                )
                await db.commit()
                return True
        except Exception:
            return False

    async def get_usdt_wallet(self) -> Optional[str]:
        try:
            async with aiosqlite.connect(self.db_path) as db:
                async with db.execute('SELECT usdt_wallet FROM settings WHERE id = 1') as cursor:
                    row = await cursor.fetchone()
                    return row[0] if row else None
        except Exception:
            return None

    async def add_custom_product(
        self,
        category: str,
        name: str,
        price_rub: int = None,
        price_usd: int = None,
        description: str = None
    ) -> bool:
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    '''INSERT INTO products
                    (category, name, price_rub, price_usd, description, availability)
                    VALUES (?, ?, ?, ?, ?, 1)''',
                    (category, name, price_rub, price_usd, description)
                )
                await db.commit()
                return True
        except Exception:
            return False

    async def delete_custom_product(self, product_id: int) -> bool:
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute('DELETE FROM products WHERE id = ?', (product_id,))
                await db.commit()
                return True
        except Exception:
            return False

    async def get_custom_products(self) -> List[Dict[str, Any]]:
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                async with db.execute(
                    'SELECT * FROM products WHERE availability = 1 ORDER BY category, name'
                ) as cursor:
                    rows = await cursor.fetchall()
                    return [dict(row) for row in rows]
        except Exception:
            return []

    async def get_product_by_id(self, product_id: int) -> Optional[Dict[str, Any]]:
        try:
            async with aiosqlite.connect(self.db_path) as db:
                db.row_factory = aiosqlite.Row
                async with db.execute(
                    'SELECT * FROM products WHERE id = ?', (product_id,)
                ) as cursor:
                    row = await cursor.fetchone()
                    return dict(row) if row else None
        except Exception:
            return None

    async def update_product_availability(self, product_id: int, available: bool) -> bool:
        try:
            async with aiosqlite.connect(self.db_path) as db:
                await db.execute(
                    'UPDATE products SET availability = ? WHERE id = ?',
                    (1 if available else 0, product_id)
                )
                await db.commit()
                return True
        except Exception:
            return False

    async def get_categories_with_products(self) -> List[str]:
        try:
            async with aiosqlite.connect(self.db_path) as db:
                async with db.execute(
                    'SELECT DISTINCT category FROM products WHERE availability = 1'
                ) as cursor:
                    rows = await cursor.fetchall()
                    return [row[0] for row in rows]
        except Exception:
            return []