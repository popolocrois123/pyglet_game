from customer import Customer
import time
import pyglet
from simple_mover import SimpleMover

class CustomerManager:
    def __init__(self, parent, num_customers=2, log_func=None):
        self.parent = parent
        self.log = log_func if log_func else lambda msg: None  # ログがなければ無効化

        # self.window_height = parent.window_height
        self.batch = self.parent.batch
        # # 入口の位置
        # self.entrance_pos = parent.map.get_entrance_positions()
        self.simple_mover = SimpleMover((1, 1), (10, 1), 
                                        batch=self.batch,
                                        log_func=self.log)

    def update(self, dt):
        self.simple_mover.update(dt)