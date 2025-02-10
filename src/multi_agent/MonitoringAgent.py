from src.multi_agent.Agent import Agent
from langchain_core.messages import HumanMessage
import json
class MonitoringAgent(Agent):
    # def __init__(self, name, llm):
    #     super().__init__(name, llm)

    def process_message(self, message):
        # 模拟获取监控数据
        mock_data = {
            "cpu_usage": 95,
            "memory_usage": 80,
            "disk_io": 1200
        }

        # 使用LLM判断异常
        prompt = f"""当前监控数据：{json.dumps(mock_data)}
        请判断是否存在异常，返回JSON格式：
        {{"status": "normal|warning|critical", "description": "..."}}"""

        response = self.llm([HumanMessage(content=prompt)])
        result = json.loads(response.content)

        if result["status"] != "normal":
            print(f"[{self.name}] 检测到异常：{result['description']}")
            # 触发后续处理流程
            self.coordinator.dispatch({
                "type": "alert",
                "data": mock_data,
                "analysis": result
            })