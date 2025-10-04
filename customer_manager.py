from customer import Customer
import time
import pyglet
from simple_mover import SimpleMover
import random
import queue

class CustomerManager:
    def __init__(self, parent, map_data, map, num_customers=5, log_func=None):
        self.parent = parent
        self.log = log_func if log_func else lambda msg: None  # ログがなければ無効化

        # self.window_height = parent.window_height
        self.batch = self.parent.batch

        # map_dataの取得
        self.map_data = map_data

        # mapクラスの呼び出し
        self.map = map

        # yの計算
        self.real_grid_y = len(self.map_data)

        # ランダムエリアを取得
        self.general_area = self.parent.map.general_costomer_area
        # print(self.general)

        # # 入口の位置
        # self.entrance_pos = parent.map.get_entrance_positions()
        
        self.customers = [] # 顧客本体のリスト

        # 初期顧客数
        self.num_customers_to_initialize = num_customers

        # キャラのキューを作成
        self.chara_queue = queue.Queue()

        # 新規顧客の生成
        self.spawn_timer = 0.0
        self.spawn_interval = 5 # 5秒ごとに新しい顧客を生成
        self.max_customers = 10   # 任意：上限を設定したい場合

        # 初期顧客
        self.setup_initial_customers()

        # 客のターゲット座標のリスト
        self.target_list = []


    # 初期顧客の生成
    def setup_initial_customers(self):
        # ⭐ 初期顧客を spawn_customer() 経由で生成
        for _ in range(self.num_customers_to_initialize):
            self.spawn_customer()

    def update(self, dt):
        # self.simple_mover.update(dt)
        # for cu in self.customers:
        #     # self.setup_target()
        #     self.setup_target(cu)
        self.assign_entrance()
        self.move_to_entrance(dt)



    # 顧客生成
    def spawn_customer(self):
        # general_area: 生成エリア　から取り出す
        random_G = random.choice(self.general_area) if self.general_area else None
        # マップのグリッドサイズの取得
        row_grid = len(self.map_data)
        # タプルからxとyを取り出す
        # xはそのままで
        x = random_G[0]
        # データの原点は左上、ゲームは左下が原点なのでそのためにy座標を変換する
        y = row_grid - random_G[1] - 1
        # gridにx,yを代入する
        grid = (x, y)

        # 状態を決める
        # 顧客生成(店外)
        state = "outside"



        # 生成する直後は動かないのでスタート位置とゴール位置を同じにする
        simple_mover = SimpleMover(grid, grid,
                                    state, self.map,
                                    batch=self.batch,
                                    log_func=self.log)


        # そのインスタンスをリストの中にいれて管理する
        self.customers.append(simple_mover)
        # 生成する時に生成するエリアを決める

        # ログで確認
        self.log(f"【顧客生成】pos: {random_G} state: {state}")

        # 何個生成するかのmaxを決める
        
        # 生成するスパン
        # （例えば10秒で生成など）

    # 生成した客のターゲット座標の設定
    # def setup_target(self, cu):
    #     cu.target_x = 17
    #     cu.target_y = 2

    # 入り口までアサインする（受付）
    def assign_entrance(self):
        for cu in self.customers:
            if cu.state == "outside":
                # self.setup_target()
                # アンパックする
                # self.log(f"{self.map.entrance_pos}")
                x, y = self.map.entrance_pos
                y = self.real_grid_y - (y + 1)
                cu.setup_new_target(x, y)
                # self.setup_target(cu)
                # cu.update(dt)
                cu.state = "moving_to_entrance"
        

                # ログで確認
                self.log(f"【入り口でアサインする】pos: {x, y} state: {cu.state}")

        # cu.target_x = 17
        # cu.target_y = 2

    def move_to_entrance(self, dt):
        for cu in self.customers:
            if cu.state == "moving_to_entrance":
                cu.update(dt)
                # キャラのキューに追加
                self.chara_queue.put(cu)


