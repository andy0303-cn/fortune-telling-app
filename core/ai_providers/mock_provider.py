from typing import Dict, Any
from .base import BaseAIProvider
from ..prompts import FORTUNE_KNOWLEDGE_BASE, FORTUNE_MASTER_PROMPT, RESPONSE_FORMAT
import random
import traceback
from datetime import datetime

class MockProvider(BaseAIProvider):
    """模拟的 AI Provider，提供高质量的模拟数据"""
    
    def generate_fortune(self, user_data: Dict[str, Any]) -> str:
        """根据用户信息生成个性化的运势分析"""
        print("\n=== Starting fortune generation ===")
        
        # 检查数据完整性
        required_fields = ['name', 'gender', 'birthDate', 'birthPlace']
        for field in required_fields:
            if not user_data.get(field):
                raise ValueError(f"Missing required field: {field}")
        
        title = "先生" if user_data.get('gender') == 'M' else "女士"
        name = user_data.get('name')
        birth_date = user_data.get('birthDate')
        birth_place = user_data.get('birthPlace')
        
        print(f"Processing user info: name={name}, gender={user_data.get('gender')}, birth_date={birth_date}, birth_place={birth_place}")
        
        # 处理日期格式
        date_part = birth_date.split(' ')[0]  # 先分离日期和时间
        time_part = birth_date.split(' ')[1]
        
        # 处理日期部分
        if '/' in date_part:
            year, month, day = map(int, date_part.split('/'))
        elif '-' in date_part:
            year, month, day = map(int, date_part.split('-'))
        else:
            raise ValueError(f"Unsupported date format: {date_part}")
        
        # 处理时间部分
        hour = int(time_part.split(':')[0])
        
        print(f"Successfully parsed date: year={year}, month={month}, day={day}, hour={hour}")
        
        # 计算生肖和星座
        zodiac = self._get_chinese_zodiac(year)
        constellation = self._get_constellation(month, day)
        
        print(f"Calculated: zodiac={zodiac}, constellation={constellation}")
        
        # 获取命理分析
        bazi = self._get_bazi(year, month, day, hour)
        five_elements = self._get_five_elements_analysis(year, month)
        zodiac_compatibility = self._get_zodiac_compatibility(zodiac)
        
        print(f"Generated analysis: bazi={bazi}, five_elements={five_elements}")
        
        # 获取当前年份信息
        current_year = datetime.now().year
        current_zodiac = "蛇"  # 2025年是蛇年
        
        # 分析与当年的关系
        year_relation = self._analyze_year_relation(zodiac, current_zodiac)
        
        # 生成个性化内容
        result = f"""【整体运势】：尊敬的{name}{title}，您{year}年生于{month}月{day}日{hour}时{birth_place}。八字为{bazi}，{five_elements}。在2025乙巳年，{year_relation}。作为{zodiac}年出生的{constellation}座，您天生具有{self._get_zodiac_traits(zodiac)}的特质，同时也兼具{self._get_constellation_traits(constellation)}的性格。近期运势走向积极，尤其在{self._get_lucky_aspects(zodiac, constellation)}方面有显著提升。建议您充分发挥{zodiac}的{self._get_zodiac_advantages(zodiac)}优势，把握机遇，稳步向前。

【事业运势】：基于您的八字命理，近期事业运势{self._get_career_trend(zodiac, constellation)}。您的{self._get_career_strengths()}特质将在工作中发挥重要作用。{self._get_career_advice(zodiac, constellation)}。

【财运分析】：从五行属性来看，您的财运受{self._get_five_elements_influence(year)}影响。{self._get_wealth_tips(month)}。理财建议：{self._get_financial_advice()}。要特别注意{self._get_financial_warnings()}。

【感情运势】：命理显示您{zodiac_compatibility}。{self._get_love_fortune(zodiac, constellation, user_data)}。在感情互动中，建议{self._get_relationship_tips()}。{self._get_love_advice(user_data)}。

【健康提醒】：根据五行养生理论，{self._get_health_advice_by_elements(year)}。{self._get_health_tips()}。特别要注意{self._get_health_warnings_by_zodiac(zodiac)}。

【人际关系】：紫微斗数显示，您的贵人位在{self._get_lucky_direction(year)}方向。{self._get_social_advice()}。建议您{self._get_social_tips()}，以增进人际缘分。"""
        
        print("Successfully generated personalized content")
        return result

    def _get_chinese_zodiac(self, year: int) -> str:
        zodiac_animals = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]
        return zodiac_animals[(year - 1900) % 12]

    def _get_constellation(self, month: int, day: int) -> str:
        """获取星座"""
        dates = (
            (1, 20, "摩羯"), (2, 19, "水瓶"), (3, 21, "双鱼"),
            (4, 20, "白羊"), (5, 21, "金牛"), (6, 22, "双子"),
            (7, 23, "巨蟹"), (8, 23, "狮子"), (9, 23, "处女"),
            (10, 24, "天秤"), (11, 23, "天蝎"), (12, 22, "射手")
        )
        
        if month == 12 and day > 22:
            return "摩羯"
        
        for next_month, day_limit, constellation in dates:
            if month == next_month and day < day_limit:
                return dates[next_month - 2][2]  # 返回上个月的星座
            if month < next_month:
                return dates[month - 1][2]
        return "摩羯"  # 12月默认

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

    def _get_career_advice(self, zodiac: str, constellation: str) -> str:
        """获取事业建议"""
        advice = [
            f"受{zodiac}年的影响，适合开拓创新，尝试新的领域",
            f"借{constellation}座的星运，可以在专业领域深耕发展",
            "注重团队协作，提升领导能力",
            "把握进修机会，提升专业技能"
        ]
        return random.choice(advice)

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
        """获取默认响应"""
        return """
【整体运势】：运势平稳向上，保持积极心态，把握机遇。

【事业运势】：工作发展顺利，注意提升专业能力，保持良好的团队协作。

【财运分析】：财务状况稳定，建议合理规划支出，关注长期投资。

【感情运势】：感情生活和谐，保持真诚态度，增进情感交流。

【健康提醒】：身体状况良好，注意作息规律，保持适度运动。

【人际关系】：人际关系融洽，多参与社交活动，深化重要友谊。
"""

    def _get_zodiac_traits(self, zodiac: str) -> str:
        """获取生肖特质"""
        traits = {
            "鼠": "机智灵活、善于社交",
            "牛": "勤恳踏实、意志坚定",
            "虎": "勇敢威严、充满领导力",
            "兔": "温和谦逊、优雅随和",
            "龙": "自信豪迈、充满魅力",
            "蛇": "智慧敏锐、深谋远虑",
            "马": "活力四射、追求自由",
            "羊": "温顺善良、富有同情心",
            "猴": "聪明机灵、创新求变",
            "鸡": "勤奋务实、注重细节",
            "狗": "忠诚可靠、正直善良",
            "猪": "真诚厚道、心地善良"
        }
        return traits.get(zodiac, "独特优秀")

    def _get_constellation_traits(self, constellation: str) -> str:
        """获取星座特质"""
        traits = {
            "白羊": "充满活力、勇于开拓",
            "金牛": "稳重可靠、意志坚定",
            "双子": "思维敏捷、善于沟通",
            "巨蟹": "重情重义、关怀他人",
            "狮子": "自信阳光、领导能力强",
            "处女": "完美主义、注重细节",
            "天秤": "优雅和谐、追求平衡",
            "天蝎": "神秘深邃、洞察力强",
            "射手": "乐观开朗、追求自由",
            "摩羯": "务实稳重、目标明确",
            "水瓶": "独特创新、思维前卫",
            "双鱼": "浪漫多情、富有同理心"
        }
        return traits.get(constellation, "独特优秀")

    def _get_lucky_aspects(self, zodiac: str, constellation: str) -> str:
        """获取幸运方面"""
        aspects = [
            "事业发展", "财富积累", "人际关系",
            "学习进修", "创新项目", "团队合作",
            "个人成长", "感情发展"
        ]
        return "、".join(random.sample(aspects, 2))

    def _get_zodiac_advantages(self, zodiac: str) -> str:
        """获取生肖优势"""
        advantages = {
            "鼠": "人脉资源和社交能力",
            "牛": "执行力和耐心",
            "虎": "领导才能和魄力",
            "兔": "人际关系和审美能力",
            "龙": "威望和创造力",
            "蛇": "智慧和洞察力",
            "马": "行动力和适应能力",
            "羊": "艺术天赋和亲和力",
            "猴": "应变能力和创新思维",
            "鸡": "规划能力和专注力",
            "狗": "忠诚度和执行力",
            "猪": "贵人缘和好运势"
        }
        return advantages.get(zodiac, "独特优势")

    def _get_career_trend(self, zodiac: str, constellation: str) -> str:
        """获取事业发展趋势"""
        trends = [
            f"受{zodiac}年的进取之力加持，呈现稳步上升态势",
            f"在{constellation}座的职场星运影响下，有望获得重要突破",
            "整体向好，将迎来关键的发展机遇",
            "稳中有进，适合开展新的事业计划"
        ]
        return random.choice(trends)

    def _get_five_elements_influence(self, birth_year: int) -> str:
        """获取五行对财运的影响"""
        elements = ["金", "木", "水", "火", "土"]
        element = elements[(birth_year - 1900) % 5]
        influences = {
            "金": "金属运势影响，适合稳健投资和资产积累",
            "木": "木性运势影响，有利于事业发展带来的收益",
            "水": "水行运势影响，财源广进，注意节制开支",
            "火": "火性运势影响，创业投资机会增多",
            "土": "土性运势影响，适合房产投资和稳健理财"
        }
        return influences[element]

    def _get_love_fortune(self, zodiac: str, constellation: str, user_data: Dict[str, Any]) -> str:
        """获取感情运势"""
        base_fortunes = [
            f"作为{zodiac}年的{constellation}座，您的感情生活将进入新阶段",
            f"{constellation}座的浪漫特质与{zodiac}的专一品格相得益彰",
            "桃花运势渐入佳境，易获得良缘",
            "感情发展稳定，适合深化关系"
        ]
        return random.choice(base_fortunes)

    def _get_health_advice_by_elements(self, birth_year: int) -> str:
        """基于五行提供健康建议"""
        elements = ["金", "木", "水", "火", "土"]
        element = elements[(birth_year - 1900) % 5]
        advice = {
            "金": "需要注意呼吸系统保养，适合练习太极养生",
            "木": "注意肝胆保健，建议规律作息和饮食",
            "水": "需要调节肾气，注意保暖和充足休息",
            "火": "注意心脑血管健康，建议适度运动",
            "土": "关注消化系统，注意饮食规律"
        }
        return advice[element]

    def _get_health_warnings_by_zodiac(self, zodiac: str) -> str:
        """基于生肖提供健康警示"""
        warnings = {
            "鼠": "注意神经紧张和失眠问题",
            "牛": "当心腰背劳损",
            "虎": "注意血压调节",
            "兔": "警惕胃部不适",
            "龙": "注意颈椎保养",
            "蛇": "预防心脑血管问题",
            "马": "注意运动损伤",
            "羊": "警惕呼吸系统疾病",
            "猴": "注意消化系统保养",
            "鸡": "当心内分泌失调",
            "狗": "注意关节保养",
            "猪": "警惕代谢问题"
        }
        return warnings[zodiac]

    def _get_lucky_direction(self, birth_year: int) -> str:
        """获取吉位方向"""
        directions = ["东", "南", "西", "北", "东南", "西南", "东北", "西北"]
        return random.choice(directions)

    def _get_bazi(self, birth_year: int, birth_month: int, birth_day: int, birth_hour: int) -> str:
        """计算八字"""
        heavenly_stems = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        earthly_branches = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        
        year_stem = heavenly_stems[(birth_year - 4) % 10]
        year_branch = earthly_branches[(birth_year - 4) % 12]
        
        return f"{year_stem}{year_branch}"

    def _get_five_elements_analysis(self, birth_year: int, birth_month: int) -> str:
        """详细的五行分析"""
        elements = {
            "金": ["果断", "坚毅", "威严"],
            "木": ["仁德", "创新", "进取"],
            "水": ["智慧", "灵活", "交际"],
            "火": ["热情", "直率", "领导"],
            "土": ["稳重", "诚实", "包容"]
        }
        
        year_element = ["木", "木", "火", "火", "土", "土", "金", "金", "水", "水"][(birth_year - 4) % 10]
        month_element = ["水", "水", "木", "木", "木", "火", "火", "土", "土", "金", "金", "水"][birth_month - 1]
        
        return f"{year_element}年{month_element}月生，具有{', '.join(elements[year_element])}的特质，兼具{', '.join(elements[month_element])}的性格"

    def _get_zodiac_compatibility(self, zodiac: str) -> str:
        """生肖相配分析"""
        compatibilities = {
            "鼠": ["龙", "猴"],
            "牛": ["蛇", "鸡"],
            "虎": ["马", "狗"],
            "兔": ["羊", "猪"],
            "龙": ["鼠", "猴"],
            "蛇": ["牛", "鸡"],
            "马": ["虎", "狗"],
            "羊": ["兔", "猪"],
            "猴": ["鼠", "龙"],
            "鸡": ["牛", "蛇"],
            "狗": ["虎", "马"],
            "猪": ["兔", "羊"]
        }
        return f"与{'、'.join(compatibilities[zodiac])}生肖最为相配"

    def _analyze_year_relation(self, zodiac: str, current_zodiac: str) -> str:
        # 实现年份关系的分析逻辑
        # 这里可以根据实际需求进行实现
        return "关系良好"  # 临时返回，实际实现需要根据年份关系逻辑

    def _get_year_relation(self, zodiac: str, current_zodiac: str) -> str:
        # 实现年份关系的获取逻辑
        # 这里可以根据实际需求进行实现
        return "关系良好"  # 临时返回，实际实现需要根据年份关系逻辑 