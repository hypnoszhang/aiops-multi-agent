# Logger.py

import logging
import logging.handlers


class Logger:
    def __init__(self, name, log_output="console", level="INFO"):
        self.name = name
        self.logger = logging.getLogger(name)
        self.logLevel = level
        self.file_handler = self.get_log_file()
        self.log_output = log_output
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.setup_logger()

    def log_to_console(self):
        # 创建控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.logLevel)
        console_handler.setFormatter(self.formatter)
        # 将处理器添加到日志记录器
        self.logger.addHandler(console_handler)

    def log_to_file(self):
        # 创建时间轮转文件处理器
        # 每天切分一次，保留5天内的文件
        time_rotating_handler = logging.handlers.TimedRotatingFileHandler(
            self.file_handler,
            when='midnight',  # 每天午夜切分
            interval=1,  # 每天一次
            backupCount=5  # 保留5天内的文件
        )
        time_rotating_handler.setLevel(self.logLevel)
        time_rotating_handler.setFormatter(self.formatter)

        # 创建大小轮转文件处理器
        # 最大500MB，保留5个文件
        size_rotating_handler = logging.handlers.RotatingFileHandler(
            self.file_handler,
            maxBytes=500 * 1024 * 1024,  # 500MB
            backupCount=5  # 保留5个文件
        )
        size_rotating_handler.setLevel(self.logLevel)
        size_rotating_handler.setFormatter(self.formatter)

        # 将处理器添加到日志记录器
        self.logger.addHandler(time_rotating_handler)
        self.logger.addHandler(size_rotating_handler)

    def setup_logger(self):
        self.logger.setLevel(self.logLevel)

        # 创建格式化器

        if self.log_output == "console":
            self.log_to_console()
        elif self.log_output == "file":
            self.log_to_file()
        else:
            self.log_to_console()
            self.log_to_file()

    def get_logger(self):
        return self.logger

    @staticmethod
    def get_log_file():
        return 'tmp.log'
