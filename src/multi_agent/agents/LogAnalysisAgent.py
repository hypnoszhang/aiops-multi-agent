import json
from langchain_core.messages import HumanMessage
from src.multi_agent.Agent import Agent
from src.multi_agent.Logger import Logger

log = Logger("LogAnalysisAgent", "console", "INFO").get_logger()

class LogAnalysisAgent(Agent):
    # def __init__(self, name, llm):
    #     super().__init__(name, llm)

    def process_message(self, message):
        try:
            # 模拟日志数据
            logs = """
            ERROR 2023-10-01 14:23:45 Database connection timeout
            WARN 2023-10-01 14:24:01 High response latency (4500ms)
            """

            # 使用LLM分析日志
            prompt = f"""日志内容：
            {logs}
            请分析关键错误，返回JSON格式：
            {{"critical_errors": ["..."], "recommendations": ["..."]}}"""

            response = self.llm([HumanMessage(content=prompt)])
            analysis = json.loads(response.content)

            log.info(f"[{self.name}] 日志分析结果：{analysis}")
            self.coordinator.dispatch({
                "type": "log_analysis",
                "results": analysis
            })
        except Exception as e:
            log.error(f"[{self.name}] Error: {e}")
            self.coordinator.dispatch({
                "type": "log_analysis",
                "results": {
                    "critical_errors": [],
                    "recommendations": []
                }
            })