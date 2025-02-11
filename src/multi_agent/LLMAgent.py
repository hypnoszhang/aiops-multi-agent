import time
# from langchain.chat_models import ChatOpenAI
# from langchain_community.chat_models import ChatOpenAI
from langchain_openai.chat_models import ChatOpenAI  # 更新导入语句
from src.multi_agent.agents.LogAnalysisAgent import LogAnalysisAgent
from src.multi_agent.agents.MonitoringAgent import MonitoringAgent
from src.multi_agent.agents.DiagnosisAgent import DiagnosisAgent
from src.multi_agent.Coordinator import Coordinator
from src.multi_agent.Logger import Logger

log = Logger("LLMAgent", "console", "INFO").get_logger()

if __name__ == "__main__":
    try:
        log.info(" initializing LLM environment...")
        llm = ChatOpenAI(
                        temperature=0,
                        model_name="gpt-4",
                        max_tokens=100,
                        openai_api_key="sk-CO5HolWE6Hlsw0hcZeVZKERoS651Pows8ihxomrPk2LQqQrv",
                        openai_api_base="http://bdi-gpt-stg.myhll.cn/gpt-4",
                    )
        coordinator = Coordinator()
        # 创建Agent实例
        agents = {
            "monitoring": MonitoringAgent("Monitoring", llm, coordinator),
            "log_analysis": LogAnalysisAgent("LogAnalysis", llm, coordinator),
            "diagnosis": DiagnosisAgent("Diagnosis", llm, coordinator)
        }
        log.info("registering agents")
        # 注册Agent到协调器
        for agent in agents.values():
            coordinator.register_agent(agent)
            agent.start()


        # 模拟触发监控检查
        agents["monitoring"].receive_message("check")

        # 运行10秒后停止
        time.sleep(10)
        for agent in agents.values():
            agent.stop()
    except ValueError as e:
        log.error(f" Value Error: {e}")
    except TypeError as e1:
        log.error(f"Error: {e1}")
    except Exception as e3:
        log.error("An error occurred", e3)