from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseAIProvider(ABC):
    """AI Provider 基类"""
    
    @abstractmethod
    def generate_fortune(self, user_data: Dict[str, Any]) -> str:
        """生成运势分析"""
        pass 