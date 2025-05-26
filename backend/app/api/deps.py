from typing import Optional
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db

async def get_current_user_optional():
    # 認証は後で実装
    return None
