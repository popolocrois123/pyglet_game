from customer import Customer
import time
import pyglet
from simple_mover import SimpleMover
import random

class CustomerManager:
    def __init__(self, parent, map_data, num_customers=2, log_func=None):
        self.parent = parent
        self.log = log_func if log_func else lambda msg: None  # ログがなければ無効化

        # self.window_height = parent.window_height
        self.batch = self.parent.batch

        # map_dataの取得
        self.map_data = map_data

        # # 入口の位置
        # self.entrance_pos = parent.map.get_entrance_positions()
        
        self.customers = [] # 顧客本体のリスト

        # 初期顧客数
        self.num_customers_to_initialize = num_customers

        # 新規顧客の生成
        self.spawn_timer = 0.0
        self.spawn_interval = 5 # 5秒ごとに新しい顧客を生成
        self.max_customers = 10   # 任意：上限を設定したい場合

        # 初期顧客
        self.setup_initial_customers()


    # 初期顧客の生成
    def setup_initial_customers(self):
        # ⭐ 初期顧客を spawn_customer() 経由で生成
        for ct in range(self.num_customers_to_initialize):
            self.spawn_customer(ct)

    def update(self, dt):
        # self.simple_mover.update(dt)
        pass

    # 顧客生成
    def spawn_customer(self, count):
        # マップのグリッドサイズの取得
        row_grid = len(self.map_data)
        # マップクラスのエリアを取得する
        self.map_data_F = [(x, row_grid - y - 1) for y, row in enumerate(self.map_data) 
                           for x, cell in enumerate(self.map_data[y]) 
                           if cell == "F"]
        # print(self.map_data_F)
        # 決めた場所、ランダムの座標を決める
        random_cell = random.randrange(1, 18)
        random_row = random.randrange(12, 14)

        customer_pos = [(random_cell, random_row), (17, 2)]

        # 状態を決める
        # 顧客生成(店外)
        state = "outside"

        # customerのインスタンスを作成する
        # customer = Customer(customer_pos, state, 
        #                     self.window_height, self.cell_size, 
        #                     self.color, self.batch)
        
        simple_mover = SimpleMover(customer_pos[count], customer_pos[count], 
                                    state,
                                    batch=self.batch,
                                    log_func=self.log)


        # そのインスタンスをリストの中にいれて管理する
        self.customers.append(simple_mover)
        # 生成する時に生成するエリアを決める

        # ログで確認
        self.log(f"【顧客生成】pos: {customer_pos} state: {state}")

        # 何個生成するかのmaxを決める
        
        # 生成するスパン
        # （例えば10秒で生成など）
