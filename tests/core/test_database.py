import pytest
from sqlalchemy import text

from app.core.database import sessionmanager


@pytest.mark.asyncio
async def test_database_connection():
    sessionmanager.init_db()
    async with sessionmanager.connect() as conn:
        result = await conn.execute(text("SELECT 1"))
        assert result.scalar() == 1
