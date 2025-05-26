from typing import List, Tuple, Dict, Any
import numpy as np
from openai import AsyncAzureOpenAI
import structlog
import hashlib

from app.config import settings
from app.core.cache import redis_client

logger = structlog.get_logger()

class EmbeddingService:
    def __init__(self):
        self.client = AsyncAzureOpenAI(
            api_key=settings.AZURE_OPENAI_EMBEDDING_API_KEY,
            api_version=settings.AZURE_OPENAI_API_VERSION,
            azure_endpoint=settings.AZURE_OPENAI_EMBEDDING_ENDPOINT
        )
        self.deployment_name = settings.AZURE_OPENAI_EMBEDDING_DEPLOYMENT
    
    async def generate_embedding(self, text: str) -> np.ndarray:
        cache_key = self._generate_cache_key(text)
        cached = await redis_client.get(cache_key)
        if cached:
            return np.array(cached)
        
        try:
            response = await self.client.embeddings.create(
                model=self.deployment_name,
                input=text
            )
            
            embedding = response.data[0].embedding
            embedding_array = np.array(embedding, dtype=np.float32)
            
            await redis_client.set(
                cache_key, 
                embedding_array.tolist(), 
                ttl=86400
            )
            
            return embedding_array
            
        except Exception as e:
            logger.error("Embedding generation failed", error=str(e))
            # ダミーのembeddingを返す
            return np.random.rand(1536).astype(np.float32)
    
    async def generate_mood_embedding(self, mood_input: Dict[str, Any]) -> Tuple[np.ndarray, str]:
        mood_parts = []
        
        if mood_input.get('presets'):
            preset_mapping = {
                'relaxed': 'リラックスしたい',
                'active': 'アクティブに動きたい',
                'adventure': '冒険したい',
                'gourmet': '美味しいものを食べたい',
                'culture': '文化や芸術に触れたい',
                'nature': '自然を感じたい',
                'shopping': 'ショッピングを楽しみたい',
                'romantic': 'ロマンチックな時間を過ごしたい'
            }
            
            for preset in mood_input['presets']:
                if preset in preset_mapping:
                    mood_parts.append(preset_mapping[preset])
        
        if mood_input.get('text'):
            mood_parts.append(mood_input['text'])
        
        exploration_score = mood_input.get('exploration_score', 0.5)
        if exploration_score > 0.7:
            mood_parts.append("新しい発見を求めている")
        elif exploration_score < 0.3:
            mood_parts.append("定番の人気スポットを楽しみたい")
        
        enhanced_mood_text = "。".join(mood_parts)
        embedding = await self.generate_embedding(enhanced_mood_text)
        
        return embedding, enhanced_mood_text
    
    def calculate_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return float(dot_product / (norm1 * norm2))
    
    def _generate_cache_key(self, text: str) -> str:
        hash_value = hashlib.md5(text.encode()).hexdigest()
        return f"embedding:{hash_value}"
