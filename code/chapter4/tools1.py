
import os
from typing import Dict, Any

from serpapi import SerpApiClient



def search(query: str) -> str:
    """
    一个基于SerpAPi的实战网页搜索引擎工具
    """
    print(f"正在执行[SerpApi]网页搜索:{query}")
    try:
        api_key = os.getenv("SERPAPI_API_KEY")
        if not api_key:
            return "错误:没有key 请检查"
        params = {
            "engine" : "google",
            "q":query,
            "api_key" : api_key,
            "gl": "cn", #国家代码
            "hl": "zh-cn" #语言代码
        }
        client = SerpApiClient(params)
        results = client.get_dict()

        # 智能解析:优先寻找最直接的答案
        if "answer_box_list" in results:
            return "\n".join(results["answer_box_list"])
        if "answer_box" in results and "answer" in results["answer_box"]:
            return results["answer_box"]["answer"]
        if "knowledge_graph" in results and "description" in results["knowledge_graph"]:
            return results["knowledge_graph"]["description"]
        if "organic_results" in results and results["organic_results"]:
            # 如果没有直接答案，则返回前三个有机结果的摘要
            snippets = [
                f"[{i + 1}] {res.get('title', '')}\n{res.get('snippet', '')}"
                for i, res in enumerate(results["organic_results"][:3])
            ]
            return "\n\n".join(snippets)

        return f"对不起，没有找到关于 '{query}' 的信息。"

    except Exception as e:
        return f"搜索时发生错误: {e}"

class ToolExecutor:
    """
    一个工具执行器， 负责管理和执行工具
    """

    def __init__(self):
        self.tools: Dict[str, Dict[str, Any]] = {}

    def register(self, name: str, description: str, func: callable):
        """
        像工具箱里注册一个新函数
        """
        if name in self.tools:
            print(f"警告：工具'{name}'已存在，将被覆盖")

