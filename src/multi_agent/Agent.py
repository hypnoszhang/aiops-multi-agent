from queue import Queue
import threading
import time
from src.multi_agent.Coordinator import Coordinator
import json

# Agent基础类
class Agent(threading.Thread):
    def __init__(self, name, llm):
        super().__init__()
        self.name = name
        self.llm = llm
        self.message_queue = Queue()
        self.running = True
        self.coordinator =Coordinator()

    def receive_message(self, message):
        self.message_queue.put(message)

    def stop(self):
        self.running = False

    def run(self):
        while self.running:
            if not self.message_queue.empty():
                message = self.message_queue.get()
                self.process_message(message)
            time.sleep(0.1)

    def process_message(self, message):
        pass