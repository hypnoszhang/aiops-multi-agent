import time
from langchain.chat_models import ChatOpenAI
from src.multi_agent.LogAnalysisAgent import LogAnalysisAgent
from src.multi_agent.MonitoringAgent import MonitoringAgent
from src.multi_agent.DiagnosisAgent import DiagnosisAgent
from src.multi_agent import Coordinator

if __name__ == "__main__":
    # 初始化LLM
    llm = ChatOpenAI(temperature=0, model_name="gpt-4", max_tokens=100)

    # 创建Agent实例
    agents = {
        "monitoring": MonitoringAgent("Monitoring", llm),
        "log_analysis": LogAnalysisAgent("LogAnalysis", llm),
        "diagnosis": DiagnosisAgent("Diagnosis", llm)
    }

    # 注册Agent到协调器
    for agent in agents.values():
        Coordinator.Coordinator().register_agent(agent)
        agent.start()

    # 模拟触发监控检查
    agents["monitoring"].receive_message("check")

    # 运行10秒后停止
    time.sleep(10)
    for agent in agents.values():
        agent.stop()