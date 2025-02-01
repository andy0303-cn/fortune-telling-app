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
            provider_type: Provider 类型，可选值：'mock', 'openai'
            
        Returns:
            BaseAIProvider: AI Provider 实例
        """
        print(f"Creating AI provider of type: {provider_type}")
        
        if provider_type == 'openai':
            return OpenAIProvider()
        elif provider_type == 'mock':
            return MockProvider()
        else:
            print(f"Unknown provider type: {provider_type}, falling back to mock")
            return MockProvider() 