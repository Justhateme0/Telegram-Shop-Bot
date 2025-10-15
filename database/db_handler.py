from .models import DatabaseManager
from config import DATABASE_URL

db = DatabaseManager(DATABASE_URL.replace("sqlite:///", ""))

async def init_database():
    await db.init_db()