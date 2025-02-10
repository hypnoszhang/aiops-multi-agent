from src.multi_agent.Agent import Agent
from langchain_core.messages import HumanMessage
from src.multi_agent.Logger import Logger
import json

log = Logger("MonitoringAgent", "console", "INFO").get_logger()
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
        try:
            # 使用LLM判断异常
            prompt = f"""当前监控数据：{json.dumps(mock_data)}
            请判断是否存在异常，返回JSON格式：
            {{"status": "normal|warning|critical", "description": "..."}}"""
            response = self.llm([HumanMessage(content=prompt)])
            result = json.loads(response.content)

            if result["status"] != "normal":
                log.info(f"[{self.name}] 检测到异常：{result['description']}")
                # 触发后续处理流程
                self.coordinator.dispatch({
                    "type": "alert",
                    "data": mock_data,
                    "analysis": result
                })
        except Exception as e:
            log.error(f"[{self.name}] 处理消息出错：{e}")
            self.coordinator.dispatch({
                "type": "alert",
                "data": mock_data,
                "analysis": {
                    "status": "normal",
                    "description": "无异常"
                }
            })