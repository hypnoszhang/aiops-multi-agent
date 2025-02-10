class Coordinator:
    def __init__(self):
        self.agents = {}

    def register_agent(self, agent):
        self.agents[agent.name] = agent

    def dispatch(self, message):
        # 基于消息类型路由
        if message["type"] == "alert":
            self.agents["LogAnalysis"].receive_message(message)
            self.agents["Diagnosis"].receive_message(message)
        elif message["type"] == "log_analysis":
            self.agents["Diagnosis"].receive_message(message)
        elif message["type"] == "diagnosis":
            self.agents["Monitoring"].receive_message(message)
