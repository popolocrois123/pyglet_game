from settings import *
from customer import Customer
import time
import pyglet

class CustomerManager:
    def __init__(self, parent, num_customers=2, log_func=None):
        self.parent = parent
        self.log = log_func if log_func else lambda msg: None  # ログがなければ無効化

        self.cell_size = CELL_SIZE
        self.window_height = parent.window_height
        self.batch = self.parent.batch