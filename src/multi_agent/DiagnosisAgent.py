import json
from langchain_core.messages import HumanMessage
from src.multi_agent.Agent import Agent

class DiagnosisAgent(Agent):
    # def __init__(self, name, llm):
    #     super().__init__(name, llm)

    def process_message(self, message):
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

        print(f"[{self.name}] 诊断结果：{diagnosis}")
        self.coordinator.dispatch({
            "type": "diagnosis",
            "results": diagnosis
        })