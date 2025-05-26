import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.area import Area
from app.models.spot import Spot
import structlog

logger = structlog.get_logger()

AREAS_DATA = [
    {
        "id": "shibuya",
        "name": "渋谷",
        "name_en": "Shibuya",
        "prefecture": "東京都",
        "region": "関東",
        "center_point": "POINT(139.7016 35.6595)",
        "characteristics": {
            "vibe": ["若者文化", "最先端", "賑やか"],
        },
        "popularity_rank": 0.95
    },
    {
        "id": "asakusa",
        "name": "浅草",
        "name_en": "Asakusa",
        "prefecture": "東京都",
        "region": "関東",
        "center_point": "POINT(139.7968 35.7148)",
        "characteristics": {
            "vibe": ["下町", "伝統", "観光地"],
        },
        "popularity_rank": 0.9
    }
]

SPOTS_DATA = [
    {
        "name": "渋谷スクランブルスクエア",
        "location": "POINT(139.7025 35.6580)",
        "area_id": "shibuya",
        "category": "展望台",
        "popularity_score": 0.9
    },
    {
        "name": "浅草寺",
        "location": "POINT(139.7966 35.7148)",
        "area_id": "asakusa",
        "category": "寺社仏閣",
        "popularity_score": 0.98
    }
]

async def seed_areas(db: AsyncSession):
    for area_data in AREAS_DATA:
        existing = await db.get(Area, area_data["id"])
        if not existing:
            area = Area(**area_data)
            db.add(area)
            logger.info(f"Created area: {area.name}")
    await db.commit()

async def seed_spots(db: AsyncSession):
    for spot_data in SPOTS_DATA:
        spot = Spot(**spot_data)
        db.add(spot)
        logger.info(f"Created spot: {spot.name}")
    await db.commit()

async def main():
    logger.info("Starting seed data insertion...")
    async with AsyncSessionLocal() as db:
        try:
            await seed_areas(db)
            await seed_spots(db)
            logger.info("Seed data insertion completed!")
        except Exception as e:
            logger.error(f"Error: {e}")
            await db.rollback()

if __name__ == "__main__":
    asyncio.run(main())
