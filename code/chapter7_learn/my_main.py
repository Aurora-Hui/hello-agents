from dotenv import load_dotenv

from my_llm import MyLLM

# 加载环境变量
load_dotenv()

# 示例化我们重写的客户端，并制定provider
llm = MyLLM(provider="modelscope")

# 准备消息
messages = [
    {"role":"user", "content":"你好请介绍一下自己"}
]

# 发起调用
response_stream = llm.think(messages)

# 打印响应
print("ModelScope Response: ")

for chunk in response_stream:
    # chunk在my_llm中已经答应过一次了 这里注释掉
    # print(chunk, end = "", flush = True)
    pass


