class Coordinator:
    def __init__(self):
        self.agents = {}

    def register_agent(self, agent):
        self.agents[agent.name] = agent

    def dispatch(self, message):
        # 基于消息类型路由
        if message["type"] == "alert":
            self.agents["log_analysis"].receive_message(message)
            self.agents["diagnosis"].receive_message(message)
        elif message["type"] == "log_analysis":
            self.agents["diagnosis"].receive_message(message)
        elif message["type"] == "diagnosis":
            self.agents["decision"].receive_message(message)


coordinator = Coordinator()