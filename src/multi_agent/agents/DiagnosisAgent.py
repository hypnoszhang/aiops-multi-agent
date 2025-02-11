import json
from langchain_core.messages import HumanMessage
from src.multi_agent.Agent import Agent
from src.multi_agent.Logger import Logger

log = Logger("DiagnosisAgent", "console", "INFO").get_logger()


class DiagnosisAgent(Agent):
    # def __init__(self, name, llm):
    #     super().__init__(name, llm)

    def process_message(self, message):
        try:
            context = f"""
            监控警报：{message['data']}
            日志分析：{message.get('log_analysis', '')}
            """

            prompt = f"""运维上下文：
            {context}
            请进行根因分析并给出诊断建议，返回JSON格式：
            {{"root_cause": "...", "confidence": 0-100, "action_steps": [...]}}"""

            response = self.llm([HumanMessage(content=prompt)])
            diagnosis = json.loads(response.content)

            log.info(f"[{self.name}] 诊断结果：{diagnosis}")
            self.coordinator.dispatch({
                "type": "diagnosis",
                "results": diagnosis
            })
        except Exception as e:
            log.error(f"[{self.name}] 诊断失败：{e}")
            self.coordinator.dispatch({
                "type": "diagnosis",
                "results": {
                    "root_cause": "无法诊断",
                    "confidence": 0,
                    "action_steps": []
                }
            })
            self.stop()
