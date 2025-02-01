from typing import Dict, Any
from .base import BaseAIProvider
import random

class MockProvider(BaseAIProvider):
    """模拟的 AI Provider，提供高质量的模拟数据"""
    
    def generate_fortune(self, user_data: Dict[str, Any]) -> str:
        """根据用户信息生成个性化的运势分析
        
        Args:
            user_data: 用户信息字典，包含：
                - name: 姓名
                - gender: 性别 ('M'/'F')
                - birthDate: 出生日期
                - birthPlace: 出生地点
        """
        # 根据性别选择不同的称呼
        title = "先生" if user_data['gender'] == 'M' else "女士"
        
        # 根据生日计算一些基本特征
        birth_month = int(user_data['birthDate'].split('-')[1])
        season = self._get_season(birth_month)
        
        return f"""
【整体运势】：{user_data['name']}{title}的整体运势稳健向上。作为{season}出生的人，您天生具有{self._get_season_traits(season)}的特质。近期运势走向积极，尤其在{self._get_lucky_aspects()}方面有较好的发展机会。

【事业运势】：{self._get_career_fortune(user_data)}

【财运分析】：{self._get_wealth_fortune(birth_month)}

【感情运势】：{self._get_love_fortune(user_data)}

【健康提醒】：{self._get_health_advice(season)}

【人际关系】：{self._get_relationship_advice(user_data)}
"""

    def _get_season(self, month: int) -> str:
        if month in [3, 4, 5]:
            return "春季"
        elif month in [6, 7, 8]:
            return "夏季"
        elif month in [9, 10, 11]:
            return "秋季"
        else:
            return "冬季"
            
    def _get_season_traits(self, season: str) -> str:
        traits = {
            "春季": "充满活力、创新进取",
            "夏季": "热情开朗、积极乐观",
            "秋季": "稳重细致、深思熟虑",
            "冬季": "沉着冷静、坚韧不拔"
        }
        return traits[season]
    
    # ... 其他辅助方法的实现 ... 