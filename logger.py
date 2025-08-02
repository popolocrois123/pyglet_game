import time
from collections import deque

# ログを記録する
class Logger:
    def __init__(self, log_file_path, max_logs=100):
        self.log_file = open(log_file_path, "w", encoding="utf-8")
        self.start_time = time.time()
        self.max_logs = max_logs
        # 最大max_logsだけ保持
        self.log_buffer = deque(maxlen=max_logs)
    
    def log(self, message:str):
        timestamp = round(time.time() - self.start_time, 2)
        log_line = f"[{timestamp} {message}]"
        self.log_buffer.append(log_line)
        self.log_file.write(log_line + "\n")
        self.log_file.flush()

    def get_recent_logs(self):
        return list(self.log_buffer)
    
    def close(self):
        self.log_file.close()