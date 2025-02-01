import os
from typing import Dict, Any
import requests
import logging
from .prompts import (
    FORTUNE_KNOWLEDGE_BASE,
    FORTUNE_MASTER_PROMPT,
    RESPONSE_FORMAT,
    SECTION_MARKERS
)
from .ai_providers.base import BaseAIProvider
from .ai_providers.openai_provider import OpenAIProvider
from .ai_providers.deepseek_provider import DeepSeekProvider
from .ai_providers.claude_provider import ClaudeProvider

class FortuneAgent:
    def __init__(self, test_mode=True, provider='claude'):
        self.test_mode = test_mode
        self.provider: BaseAIProvider = self._get_provider(provider)
        
    def _get_provider(self, provider_name: str) -> BaseAIProvider:
        providers = {
            'openai': OpenAIProvider,
            'deepseek': DeepSeekProvider,
            'claude': ClaudeProvider
        }
        return providers[provider_name]()
    
    def analyze_fortune(self, user_data: Dict[str, Any]) -> Dict[str, str]:
        """生成运势分析"""
        try:
            if self.test_mode:
                response = self._get_test_response()
            else:
                response = self.provider.generate_fortune(user_data)
            return self._parse_response(response)
        except Exception as e:
            logging.error(f"AI调用失败: {str(e)}")
            raise
            
    def _get_test_response(self) -> str:
        """返回测试数据"""
        return """
【总体运势】
2024年对你来说是一个充满机遇的年份。五行属性显示你正处于上升期，特别是在事业和个人发展方面会有突破性进展。建议把握机会，积极进取。

【事业发展】
职业发展面临新的机遇，可能会有升职或转行的机会。建议在6-8月份积极寻求新的发展方向，投资自我提升将会带来良好回报。

【财运分析】
整体财运稳定向上，尤其是在投资理财方面会有意外收获。建议适度投资，但要注意风险控制，不要过于激进。

【感情姻缘】
感情生活将会有新的突破，单身者有机会遇到心仪的对象，已婚者夫妻关系更加和睦。建议多参加社交活动，增加缘分机会。

【健康提醒】
需要注意作息规律，特别是在工作繁忙时期。建议适当运动，保持充足睡眠，注意饮食均衡，避免过度劳累。

【人际关系】
人际关系总体和谐，贵人运旺盛。工作中会得到领导赏识，生活中会结识新朋友。建议保持真诚待人的态度，维护好现有的人际网络。
"""

    def _generate_prompt(self, user_data: Dict[str, Any]) -> str:
        """生成完整的提示词"""
        return f"""
{FORTUNE_KNOWLEDGE_BASE}

{FORTUNE_MASTER_PROMPT}

{RESPONSE_FORMAT}

用户信息：
- 姓名：{user_data['name']}
- 性别：{'男' if user_data['gender'] == 'M' else '女'}
- 出生日期：{user_data['birthDate']}
- 出生地点：{user_data['birthPlace']}

请基于以上信息，按照指定格式提供完整的运势分析。记住使用【】标记每个维度，确保分析内容详实且实用。
"""

    def _call_deepseek_api(self, prompt: str) -> str:
        """调用DeepSeek API"""
        if self.test_mode:
            # 返回测试数据
            return """
【总体运势】
2024年对你来说是一个充满机遇的年份。五行属性显示你正处于上升期，特别是在事业和个人发展方面会有突破性进展。建议把握机会，积极进取。

【事业发展】
职业发展面临新的机遇，可能会有升职或转行的机会。建议在6-8月份积极寻求新的发展方向，投资自我提升将会带来良好回报。

【财运分析】
整体财运稳定向上，尤其是在投资理财方面会有意外收获。建议适度投资，但要注意风险控制，不要过于激进。

【感情姻缘】
感情生活将会有新的突破，单身者有机会遇到心仪的对象，已婚者夫妻关系更加和睦。建议多参加社交活动，增加缘分机会。

【健康提醒】
需要注意作息规律，特别是在工作繁忙时期。建议适当运动，保持充足睡眠，注意饮食均衡，避免过度劳累。

【人际关系】
人际关系总体和谐，贵人运旺盛。工作中会得到领导赏识，生活中会结识新朋友。建议保持真诚待人的态度，维护好现有的人际网络。
"""
        else:
            headers = {
                'Authorization': f'Bearer {os.getenv("DEEPSEEK_API_KEY")}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'model': 'deepseek-chat',
                'messages': [
                    {'role': 'system', 'content': '你是一位精通中西方命理的大师。'},
                    {'role': 'user', 'content': FORTUNE_KNOWLEDGE_BASE},
                    {'role': 'assistant', 'content': '我已经完全理解并掌握了这些命理知识体系。'},
                    {'role': 'user', 'content': prompt}
                ],
                'temperature': 0.7,
                'max_tokens': 4000  # 增加token限制以容纳更多内容
            }
            
            response = requests.post(
                'https://api.deepseek.com/v1/chat/completions',
                headers=headers,
                json=data
            )
            
            if response.status_code != 200:
                raise Exception(f"API调用失败: {response.text}")
            
            return response.json()['choices'][0]['message']['content']

    def _parse_response(self, response: str) -> Dict[str, str]:
        """解析API响应"""
        result = {value: '' for value in SECTION_MARKERS.values()}
        current_section = None
        current_text = []
        
        for line in response.split('\n'):
            line = line.strip()
            if not line:
                continue
            
            # 检查是否是新的段落开始
            for cn_section, en_section in SECTION_MARKERS.items():
                if f'【{cn_section}】' in line:
                    if current_section:
                        result[current_section] = '\n'.join(current_text)
                    current_section = en_section
                    current_text = []
                    break
            else:
                if current_section:
                    current_text.append(line)
        
        if current_section and current_text:
            result[current_section] = '\n'.join(current_text)
            
        return result 