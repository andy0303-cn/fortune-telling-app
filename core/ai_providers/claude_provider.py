import os
import aiohttp
import asyncio
from typing import Dict, Any
import logging
from .base import BaseAIProvider
from ..prompts import (
    FORTUNE_KNOWLEDGE_BASE,
    FORTUNE_MASTER_PROMPT,
    RESPONSE_FORMAT
)

class ClaudeProvider(BaseAIProvider):
    def __init__(self):
        self.api_key = os.getenv('CLAUDE_API_KEY')
        self.api_url = "https://api.anthropic.com/v1/messages"
        self.proxy = os.getenv('HTTP_PROXY', 'http://127.0.0.1:7890')
        
    def generate_fortune(self, user_data: Dict[str, Any]) -> str:
        return asyncio.run(self._async_generate_fortune(user_data))
        
    async def _async_generate_fortune(self, user_data: Dict[str, Any]) -> str:
        try:
            prompt = self._generate_prompt(user_data)
            logging.debug("Generated prompt for Claude")
            
            headers = {
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            }
            
            data = {
                "model": "claude-3-opus-20240229",
                "messages": [
                    {
                        "role": "user",
                        "content": f"""你是一位精通中西方命理的大师。

{FORTUNE_KNOWLEDGE_BASE}

{FORTUNE_MASTER_PROMPT}

{RESPONSE_FORMAT}

用户信息：
- 姓名：{user_data['name']}
- 性别：{'男' if user_data['gender'] == 'M' else '女'}
- 出生日期：{user_data['birthDate']}
- 出生地点：{user_data['birthPlace']}

请基于以上信息，按照指定格式提供完整的运势分析。记住使用【】标记每个维度，确保分析内容详实且实用。"""
                    }
                ],
                "max_tokens": 4000,
                "temperature": 0.7
            }
            
            logging.debug("Sending request to Claude API...")
            
            connector = ProxyConnector.from_url(self.proxy)
            timeout = aiohttp.ClientTimeout(total=60)
            
            async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
                async with session.post(
                    self.api_url,
                    headers=headers,
                    json=data
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise Exception(f"API调用失败: {error_text}")
                    
                    result = await response.json()
                    content = result['content'][0]['text']
                    logging.debug(f"Received response from Claude API: {content[:100]}...")
                    return content
            
        except Exception as e:
            logging.error(f"Claude API调用失败: {str(e)}")
            logging.error(f"错误类型: {type(e)}")
            import traceback
            logging.error(f"堆栈跟踪: {traceback.format_exc()}")
            raise 