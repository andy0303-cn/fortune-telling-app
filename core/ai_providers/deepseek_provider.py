import os
import requests
from typing import Dict, Any
from .base import BaseAIProvider
from ..prompts import (
    FORTUNE_KNOWLEDGE_BASE,
    FORTUNE_MASTER_PROMPT,
    RESPONSE_FORMAT
)

class DeepSeekProvider(BaseAIProvider):
    def __init__(self):
        self.api_key = os.getenv('DEEPSEEK_API_KEY')
        
    def generate_fortune(self, user_data: Dict[str, Any]) -> str:
        prompt = self._generate_prompt(user_data)
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
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
            'max_tokens': 2000
        }
        
        response = requests.post(
            'https://api.deepseek.com/v1/chat/completions',
            headers=headers,
            json=data
        )
        
        if response.status_code != 200:
            raise Exception(f"API调用失败: {response.text}")
            
        return response.json()['choices'][0]['message']['content']
        
    def _generate_prompt(self, user_data: Dict[str, Any]) -> str:
        return f"""
{FORTUNE_MASTER_PROMPT}

{RESPONSE_FORMAT}

用户信息：
- 姓名：{user_data['name']}
- 性别：{'男' if user_data['gender'] == 'M' else '女'}
- 出生日期：{user_data['birthDate']}
- 出生地点：{user_data['birthPlace']}

请基于以上信息，按照指定格式提供完整的运势分析。记住使用【】标记每个维度，确保分析内容详实且实用。
""" 