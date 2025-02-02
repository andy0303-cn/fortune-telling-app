import os
from anthropic import Anthropic
from dotenv import load_dotenv

def test_claude():
    load_dotenv()
    client = Anthropic(api_key=os.getenv('CLAUDE_API_KEY'))
    
    try:
        message = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            messages=[{
                "role": "user",
                "content": "你好，这是一个测试消息。请用中文回复。"
            }]
        )
        print("✅ API 调用成功！")
        print(f"回复: {message.content}")
    except Exception as e:
        print(f"❌ 错误: {str(e)}")

if __name__ == "__main__":
    test_claude() 