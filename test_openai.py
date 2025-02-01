import os
from openai import OpenAI
from dotenv import load_dotenv

def test_openai():
    load_dotenv()
    client = OpenAI()  # 让 SDK 自动处理配置
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "你好"}]
        )
        print("✅ API 调用成功！")
        print(f"回复: {response.choices[0].message.content}")
    except Exception as e:
        print(f"❌ 错误: {str(e)}")

if __name__ == "__main__":
    test_openai() 