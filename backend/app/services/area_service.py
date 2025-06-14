from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
import numpy as np
import structlog

from app.models.area import Area
from app.models.vector import VectorData
from app.schemas.area import AreaRecommendation
from app.schemas.common import MoodInput, ConditionsInput, LocationInput
from app.core.cache import redis_client

logger = structlog.get_logger()


class AreaService:
    def __init__(self, db: AsyncSession, embedding_service, llm_service):
        self.db = db
        self.embedding_service = embedding_service
        self.llm_service = llm_service

    async def recommend_areas(
        self,
        mood_input: MoodInput,
        conditions: ConditionsInput,
        user_location: LocationInput,
    ) -> List[AreaRecommendation]:
        cache_key = self._generate_cache_key(mood_input, conditions, user_location)
        cached = await redis_client.get(cache_key)
        if cached:
            return [AreaRecommendation(**area) for area in cached]

        mood_vector, enhanced_mood = (
            await self.embedding_service.generate_mood_embedding(mood_input.dict())
        )

        candidate_areas = await self._get_candidate_areas(
            user_location, max_distance_km=50
        )

        area_scores = await self._calculate_area_scores(
            candidate_areas, mood_vector, mood_input.exploration_score
        )

        recommendations = await self.llm_service.recommend_areas(
            mood_text=enhanced_mood,
            area_candidates=area_scores[:10],
            conditions=conditions.dict(),
        )

        await redis_client.set(cache_key, [r.dict() for r in recommendations], ttl=300)

        return recommendations

    async def _get_candidate_areas(
        self, user_location: LocationInput, max_distance_km: float
    ) -> List[Area]:
        point = f"POINT({user_location.longitude} {user_location.latitude})"
        geom = func.ST_GeomFromText(point, 4326)

        # First try to fetch areas within the given distance
        query_near = (
            select(Area)
            .where(func.ST_DWithin(Area.center_point, geom, max_distance_km * 1000))
            .order_by(func.ST_Distance(Area.center_point, geom))
        )

        result = await self.db.execute(query_near)
        areas = result.scalars().all()

        # If no areas are found nearby, fallback to the closest areas regardless of distance
        if not areas:
            query_all = (
                select(Area)
                .order_by(func.ST_Distance(Area.center_point, geom))
                .limit(10)
            )
            result = await self.db.execute(query_all)
            areas = result.scalars().all()

        return areas

    async def _calculate_area_scores(
        self, areas: List[Area], mood_vector: np.ndarray, exploration_score: float
    ) -> List[dict]:
        area_scores = []

        for area in areas:
            # ダミーのスコア計算
            similarity = 0.8 + np.random.rand() * 0.2

            if exploration_score > 0.7 and area.popularity_rank:
                adjusted_score = similarity * (2 - area.popularity_rank)
            else:
                adjusted_score = similarity

            area_scores.append(
                {"area": area, "score": adjusted_score, "similarity": similarity}
            )

        area_scores.sort(key=lambda x: x["score"], reverse=True)
        return area_scores

    def _generate_cache_key(
        self, mood: MoodInput, conditions: ConditionsInput, location: LocationInput
    ) -> str:
        import hashlib
        import json

        data = {
            "mood": mood.dict(),
            "conditions": conditions.dict(),
            "location": {
                "lat": round(location.latitude, 2),
                "lon": round(location.longitude, 2),
            },
        }

        serialized = json.dumps(data, sort_keys=True)
        return f"area_rec:{hashlib.md5(serialized.encode()).hexdigest()}"
