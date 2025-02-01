import os
from openai import OpenAI  # 改回标准客户端
import httpx
from typing import Dict, Any
import logging
from .base import BaseAIProvider
from ..prompts import (
    FORTUNE_KNOWLEDGE_BASE,
    FORTUNE_MASTER_PROMPT,
    RESPONSE_FORMAT
)

class OpenAIProvider(BaseAIProvider):
    def __init__(self, fallback_provider=None):
        self.fallback_provider = fallback_provider
        
        # 只在本地开发时使用代理
        if os.getenv('FLASK_ENV') == 'development':
            proxy = os.getenv('HTTP_PROXY', 'http://127.0.0.1:7890')
            timeout = httpx.Timeout(60.0, connect=20.0)
            http_client = httpx.Client(
                proxy=proxy,
                timeout=timeout,
                verify=False
            )
        else:
            http_client = httpx.Client(
                timeout=httpx.Timeout(60.0, connect=20.0)
            )
        
        self.client = OpenAI(
            api_key=os.getenv('OPENAI_API_KEY'),
            http_client=http_client
        )
        
    def generate_fortune(self, user_data: Dict[str, Any]) -> str:
        try:
            prompt = self._generate_prompt(user_data)
            logging.debug("Generated prompt for OpenAI")
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "你是一位精通中西方命理的大师。"
                    },
                    {
                        "role": "user",
                        "content": FORTUNE_KNOWLEDGE_BASE
                    },
                    {
                        "role": "assistant",
                        "content": "我已经完全理解并掌握了这些命理知识体系。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            content = response.choices[0].message.content
            logging.debug(f"Received response from OpenAI API: {content[:100]}...")
            return content
            
        except Exception as e:
            logging.error(f"OpenAI API调用失败: {str(e)}")
            logging.error(f"错误类型: {type(e)}")
            import traceback
            logging.error(f"堆栈跟踪: {traceback.format_exc()}")
            raise
        
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