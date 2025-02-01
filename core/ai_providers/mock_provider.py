from typing import Dict, Any
from .base import BaseAIProvider

class MockProvider(BaseAIProvider):
    """模拟的 AI Provider"""
    
    def generate_fortune(self, user_data: Dict[str, Any]) -> str:
        """生成运势分析"""
        return """
【整体运势】：运势平稳向上，保持积极心态，把握机遇。

【事业运势】：工作发展顺利，注意提升专业能力，保持良好的团队协作。

【财运分析】：财务状况稳定，建议合理规划支出，关注长期投资。

【感情运势】：感情生活和谐，保持真诚态度，增进情感交流。

【健康提醒】：身体状况良好，注意作息规律，保持适度运动。

【人际关系】：人际关系融洽，多参与社交活动，深化重要友谊。
""" 