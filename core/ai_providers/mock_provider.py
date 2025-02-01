from typing import Dict, Any
from .base import BaseAIProvider
import random

class MockProvider(BaseAIProvider):
    """模拟的 AI Provider，提供高质量的模拟数据"""
    
    def generate_fortune(self, user_data: Dict[str, Any]) -> str:
        """根据用户信息生成个性化的运势分析"""
        try:
            title = "先生" if user_data.get('gender') == 'M' else "女士"
            birth_date = user_data.get('birthDate', '')
            birth_month = 1  # 默认值
            
            # 安全地解析日期
            try:
                if ' ' in birth_date:
                    birth_date = birth_date.split(' ')[0]
                if '-' in birth_date:
                    birth_month = int(birth_date.split('-')[1])
            except (IndexError, ValueError):
                pass
            
            name = user_data.get('name', '贵客')
            season = self._get_season(birth_month)
            lucky_elements = self._get_lucky_elements(season)
            career_advice = self._get_career_advice(season)
            wealth_tips = self._get_wealth_tips(birth_month)
            
            return f"""【整体运势】：尊敬的{name}{title}，从您{season}的出生时节来看，您天生具有{self._get_season_traits(season)}的特质。近期运势走向积极，尤其在{lucky_elements}方面有显著提升。建议您充分发挥{season}生人特有的优势，把握机遇，稳步向前。

【事业运势】：职业发展呈现上升趋势，{career_advice}。您的{self._get_career_strengths()}特质将在工作中发挥重要作用。注意与{self._get_cooperation_tips()}，以获得更好的发展机会。

【财运分析】：财运方面显示出良好态势，{wealth_tips}。理财建议：{self._get_financial_advice()}。要特别注意{self._get_financial_warnings()}，以确保财务稳健增长。

【感情运势】：感情生活将进入一个新的阶段。{self._get_love_advice(user_data)}。在与伴侣或潜在对象的互动中，建议{self._get_relationship_tips()}，以促进感情升温。

【健康提醒】：{self._get_health_advice(season)}。建议您{self._get_health_tips()}，保持充沛精力。特别要注意{self._get_health_warnings(season)}，以维护身心健康。

【人际关系】：人际关系将迎来新的发展机遇。{self._get_social_advice()}。在社交活动中，建议您{self._get_social_tips()}，以建立更深厚的人际连接。"""
        except Exception as e:
            # 返回更有内容的默认响应
            return self._get_default_response()

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

    def _get_lucky_elements(self, season: str) -> str:
        elements = {
            "春季": ["事业拓展", "学习进修", "创新项目"],
            "夏季": ["人际交往", "团队合作", "表现机会"],
            "秋季": ["投资理财", "技能提升", "稳定发展"],
            "冬季": ["深度思考", "战略规划", "资源积累"]
        }
        return "、".join(random.sample(elements[season], 2))

    def _get_career_advice(self, season: str) -> str:
        advice = {
            "春季": "适合开展新项目，扩展业务范围",
            "夏季": "人际关系将助力事业发展，注意把握机会",
            "秋季": "专业技能提升将带来新的发展机遇",
            "冬季": "适合深入研究和规划，为未来发展打好基础"
        }
        return advice[season]

    def _get_career_strengths(self) -> str:
        strengths = [
            "专注执行、注重细节",
            "创新思维、善于沟通",
            "分析能力、战略眼光",
            "领导才能、团队协作"
        ]
        return random.choice(strengths)

    def _get_cooperation_tips(self) -> str:
        tips = [
            "上级主管保持良好沟通，展现工作热情",
            "团队成员多交流合作，共同进步",
            "同事之间互帮互助，建立信任",
            "新同事积极交流，展现专业能力"
        ]
        return random.choice(tips)

    def _get_wealth_tips(self, month: int) -> str:
        tips = [
            "近期财运上升，可以考虑稳健的投资机会",
            "财务状况趋于稳定，适合做长远规划",
            "可能出现意外收入，但要注意理性消费",
            "投资机会增多，建议审慎评估风险"
        ]
        return random.choice(tips)

    def _get_financial_advice(self) -> str:
        advice = [
            "合理分配收入，做好预算规划",
            "关注长期投资，分散投资风险",
            "建立应急资金，保持资金流动性",
            "适度投资自我提升，提高职业价值"
        ]
        return random.choice(advice)

    def _get_financial_warnings(self) -> str:
        warnings = [
            "避免冲动消费和不必要的开支",
            "谨防高风险投资和非法集资",
            "控制信用卡使用，避免过度负债",
            "警惕投资诈骗，确保资金安全"
        ]
        return random.choice(warnings)

    def _get_love_advice(self, user_data: Dict[str, Any]) -> str:
        if user_data.get('gender') == 'M':
            return random.choice([
                "保持真诚的态度，主动表达关心",
                "展现成熟稳重的一面，增进感情交流",
                "适时表达自己的想法，建立信任关系",
                "关注对方需求，创造浪漫氛围"
            ])
        else:
            return random.choice([
                "保持独立自信，展现个人魅力",
                "适度表达情感，保持适当神秘感",
                "关注个人成长，提升内在价值",
                "保持开放心态，把握缘分机会"
            ])

    def _get_relationship_tips(self) -> str:
        return random.choice([
            "多表达关心和理解，增进感情交流",
            "创造共同话题，分享生活趣事",
            "保持适度空间，尊重彼此独立",
            "共同规划未来，建立长期目标"
        ])

    def _get_health_advice(self, season: str) -> str:
        advice = {
            "春季": "春季气温变化大，注意适时增减衣物，预防感冒",
            "夏季": "夏季注意防暑降温，保持充足水分摄入",
            "秋季": "秋季空气干燥，注意保湿润肺，预防呼吸道疾病",
            "冬季": "冬季注意保暖，预防心脑血管疾病"
        }
        return advice[season]

    def _get_health_tips(self) -> str:
        return random.choice([
            "保持规律作息，确保充足睡眠",
            "坚持适度运动，增强体质",
            "注意饮食均衡，补充营养",
            "保持心情愉悦，减轻压力"
        ])

    def _get_health_warnings(self, season: str) -> str:
        warnings = {
            "春季": "防止过敏，注意户外活动时间",
            "夏季": "避免过度疲劳，防止中暑",
            "秋季": "预防感冒，注意保暖",
            "冬季": "警惕心脑血管疾病，保持室内通风"
        }
        return warnings[season]

    def _get_social_advice(self) -> str:
        return random.choice([
            "主动参与社交活动，扩展人脉圈",
            "保持积极开放的态度，结识新朋友",
            "参加专业交流活动，提升影响力",
            "维护重要的人际关系，深化友谊"
        ])

    def _get_social_tips(self) -> str:
        return random.choice([
            "真诚待人，建立信任关系",
            "善于倾听，理解他人需求",
            "乐于分享，展现个人价值",
            "保持礼貌，尊重他人观点"
        ])

    def _get_default_response(self) -> str:
        return """
【整体运势】：运势平稳向上，保持积极心态，把握机遇。

【事业运势】：工作发展顺利，注意提升专业能力，保持良好的团队协作。

【财运分析】：财务状况稳定，建议合理规划支出，关注长期投资。

【感情运势】：感情生活和谐，保持真诚态度，增进情感交流。

【健康提醒】：身体状况良好，注意作息规律，保持适度运动。

【人际关系】：人际关系融洽，多参与社交活动，深化重要友谊。
""" 