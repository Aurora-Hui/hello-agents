import os
from dotenv import load_dotenv
from openai import OpenAI
from typing import Dict, List
# 加载env 环境变量
load_dotenv()

class HelloAgentsLLM:
    """
    LLM客户端
    调用任何兼容OpenAI接口的服务，并默认使用流式响应
    """
    def __init__(self, model: str = None, apiKey: str = None, baseUrl: str = None, timeout: int = None):
        """
        初始化客户端，优先使用传入参数，如果没提供则从环境变量加载
        """
        # 带self 就是全局变量
        self.model = model or os.getenv("LLM_MODEL_ID")
        apiKey = apiKey or os.getenv("LLM_API_KEY")
        baseUrl = baseUrl or os.getenv("LLM_BASE_URL")
        timeout = timeout or int(os.getenv("LLM_TIMEOUT", 60))

        if not all([self.model, apiKey, baseUrl]):
            raise ValueError("模型ID、API密钥和服务地址必须被提供或在.env文件中定义")
        self.client = OpenAI(api_key = apiKey, base_url = baseUrl, timeout=timeout)

    def think(self, messages: List[Dict[str, str]], temperature: float = 0) -> str:
        """
        调用大模型进行思考
        """
        print(f"正在调用{self.model} 模型...")
        try:
            response = self.client.chat.completions.create(
                model = self.model,
                messages = messages,
                temperature = temperature,
                stream = True,
            )
            # 处理流式响应
            print("大语言模型响应成功:")
            collected_content = []
            for chunk in response:
                if not chunk.choices:
                    continue
                content = chunk.choices[0].delta.content or ""
                print(content, end = "", flush = True)
                collected_content.append(content)
            print()
            return "".join(collected_content)
        except Exception as e:
            print(f"调用大模型失败 发生错误{e}")
            return None

if __name__ == "__main__":
    try:
        llmCLient = HelloAgentsLLM()
        exampleMessages = [
            {"role": "system", "content": "你是一个丰富的编程专家"},
            {"role": "user", "content": "写一个快速排序"}
        ]
        print("---调用LLM---")
        responseText = llmCLient.think(exampleMessages)
        if responseText:
            print("\n\n---完整模型响应---")
            print(responseText)
    except Exception as e:
        print(e)