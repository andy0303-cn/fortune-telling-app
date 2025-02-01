from typing import Optional
from .base import BaseAIProvider
from .mock_provider import MockProvider
from .openai_provider import OpenAIProvider

class AIProviderFactory:
    """AI Provider 工厂类"""
    
    @staticmethod
    def create_provider(provider_type: str = 'mock') -> BaseAIProvider:
        """创建 AI Provider 实例
        
        Args:
            provider_type: AI 提供者类型，可选值：mock, openai
            
        Returns:
            BaseAIProvider: AI Provider 实例
        """
        if provider_type == 'openai':
            return OpenAIProvider()
        else:
            return MockProvider()  # 默认使用模拟数据 