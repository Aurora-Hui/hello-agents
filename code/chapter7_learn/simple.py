from dotenv import load_dotenv
from hello_agents import SimpleAgent, HelloAgentsLLM

load_dotenv()

llm = HelloAgentsLLM()

# 创建simpleAgent
agent = SimpleAgent(
    name = "AI助手",
    llm = llm,
    system_prompt = "你是一个有用的AI助手"
)

# 基础对话

response = agent.run("你好！ 请介绍一下自己")
print(response)

# 添加工具功能

from hello_agents.tools import CalculatorTool
calculator = CalculatorTool()

# agent.add_tool(calculator)
response = agent.run("请帮我计算2 + 3 * 4")
print(response)

# 查看历史对话
print(f"历史消息数:{len(agent.get_history())}")