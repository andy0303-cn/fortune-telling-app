from typing import Dict, Any
from .base import BaseAIProvider

class MockProvider(BaseAIProvider):
    """模拟的 AI Provider，用于测试和开发"""
    
    def generate_fortune(self, user_data: Dict[str, Any]) -> str:
        """生成模拟的运势分析结果
        
        Args:
            user_data: 用户信息字典
            
        Returns:
            str: 格式化的运势分析结果
        """
        return f"""
【整体运势】：整体运势稳定向上，有利于个人发展和目标实现。保持积极心态，把握机遇。

【事业运势】：事业发展势头良好，有新的机会出现。工作中注意与同事协作，展现专业能力。

【财运分析】：财运平稳，适合稳健理财。避免冲动消费，关注长期投资和收益。

【感情运势】：感情生活和谐，单身者有机会遇到心仪对象。已有伴侣的感情更加稳定。

【健康提醒】：身体状况良好，但要注意作息规律，适当运动，保持充足睡眠。

【人际关系】：人际关系融洽，社交圈有所扩大。多参与集体活动，增进交流。
""" 