from typing import List, Dict, Any
import json
from openai import AsyncAzureOpenAI
import structlog

from app.config import settings
from app.schemas.area import AreaRecommendation
from app.schemas.plan import Plan

logger = structlog.get_logger()

class LLMService:
    def __init__(self):
        self.client = AsyncAzureOpenAI(
            api_key=settings.AZURE_OPENAI_API_KEY,
            api_version=settings.AZURE_OPENAI_API_VERSION,
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT
        )
        self.deployment_name = settings.AZURE_OPENAI_DEPLOYMENT_NAME
    
    async def recommend_areas(
        self,
        mood_text: str,
        area_candidates: List[dict],
        conditions: dict
    ) -> List[AreaRecommendation]:
        prompt = self._build_area_recommendation_prompt(
            mood_text, area_candidates, conditions
        )
        
        try:
            response = await self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {"role": "system", "content": "あなたは日本の旅行に詳しいコンシェルジュです。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content
            
            # JSON形式でない場合の処理
            if content.strip().startswith('{'):
                data = json.loads(content)
            else:
                # フォールバック
                return self._fallback_recommendations(area_candidates)
            
            recommendations = []
            for rec in data.get("recommendations", [])[:3]:
                recommendations.append(AreaRecommendation(**rec))
            
            return recommendations
            
        except Exception as e:
            logger.error("LLM area recommendation failed", error=str(e))
            return self._fallback_recommendations(area_candidates)
    
    def _build_area_recommendation_prompt(
        self,
        mood_text: str,
        area_candidates: List[dict],
        conditions: dict
    ) -> str:
        areas_info = "\n".join([
            f"- {area['area'].name} ({area['area'].prefecture})"
            for area in area_candidates[:10]
        ])
        
        return f"""
ユーザーの気分と条件に基づいて、最適なエリアを3つ推薦してください。

気分: {mood_text}
人数: {conditions.get('party_size', 1)}人
予算: {conditions.get('budget', 'medium')}
滞在時間: {conditions.get('duration', 8)}時間

候補エリア:
{areas_info}

JSON形式で回答してください。
"""
    
    def _fallback_recommendations(self, area_candidates: List[dict]) -> List[AreaRecommendation]:
        recommendations = []
        
        for area_data in area_candidates[:3]:
            area = area_data['area']
            recommendations.append(AreaRecommendation(
                id=area.id,
                name=area.name,
                name_en=area.name_en or area.name,
                prefecture=area.prefecture,
                region=area.region,
                match_score=0.8,
                primary_reason=f"{area.name}の魅力を体験",
                detailed_reason=f"{area.name}は、あなたの気分にぴったりのエリアです。",
                key_spots=["人気スポット1", "人気スポット2", "人気スポット3"],
                expected_experience="素敵な思い出が作れるエリアです",
                accessibility={
                    "from_user_location": "電車で約30分",
                    "ease_score": 0.8
                },
                tips="混雑を避けるなら平日がおすすめです"
            ))
        
        return recommendations
