from typing import Dict, Any
from .base import BaseAIProvider

class OpenAIProvider(BaseAIProvider):
    """OpenAI Provider"""
    
    def generate_fortune(self, user_data: Dict[str, Any]) -> str:
        """生成运势分析"""
        return "OpenAI 运势分析结果" 