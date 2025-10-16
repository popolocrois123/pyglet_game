from customer import Customer
import time
import pyglet
from simple_mover import SimpleMover
import random
import queue
from loguru import logger

class CustomerManager:
    def __init__(self, parent, map_data, map, num_customers=20, log_func=None):
        self.parent = parent
        self.log = log_func if log_func else lambda msg: None  # ログがなければ無効化

        # self.window_height = parent.window_height
        self.batch = self.parent.batch

        # map_dataの取得
        self.map_data = map_data

        # mapクラスの呼び出し
        self.map = map

        # マップの待機場所の座標のqueueを呼び出し 1つめ
        self.wait_queue = self.map.wait_queue

        # yの計算
        self.real_grid_y = len(self.map_data)

        # ランダムエリアを取得
        self.general_area = self.parent.map.general_costomer_area
        # print(self.general)

        # # 入口の位置
        # self.entrance_pos = parent.map.get_entrance_positions()
        

        

        # 初期顧客数
        self.num_customers_to_initialize = num_customers


        # 現在の客の数の管理
        self.count_num_customers = 0

        # mapのWの場所のリストを取得
        self.wait_queue = self.map.wait_queue

        # 顧客の入口での管理のためのキュー
        # 1, 待機場所管理リスト
        self.wait_chair = [False for i in range(len(self.wait_queue))]
        # print(self.wait_chair)
        # 2, 顧客本体のリスト
        self.customers = []
        # 3, 顧客と待機場所の紐づけ
        self.waiting_queue = []

        # 新規顧客の生成
        self.spawn_timer = 0.0
        self.spawn_interval = 5 # 5秒ごとに新しい顧客を生成
        self.max_customers = 8   # 任意：上限を設定したい場合

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
        # 入口まで割り当て
        self.assign_entrance()

        # 入口まで移動
        self.move_to_entrance(dt)

        # 待機場所への割り当て
        self.assign_wait_area()

        # 待機場所への移動
        self.moving_to_waiting_area(dt)


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
        
        # # カスタマーのIDを変化させる
        # simple_mover.id += 1

        # # そのインスタンスをリストの中にいれて管理する
        self.customers.append(simple_mover)

        # # 紐付けようのリストに入れる
        # self.waiting_queue.append(simple_mover)
        

        # 生成する時に生成するエリアを決める

        # ログで確認
        logger.debug(f"【顧客生成】id: {simple_mover.id} pos: {random_G} state: {state}")

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
            if (cu.state == "outside") and (self.count_num_customers <= self.max_customers):
                # self.setup_target()
                # アンパックする
                # self.log(f"{self.map.entrance_pos}")
                x, y = self.map.entrance_pos
                y = self.real_grid_y - (y + 1)
                # x, y = self.wait_queue.get()
                # y = self.real_grid_y - (y + 1)
                # print(x, y)
                # print(self.wait_queue.get())
                cu.setup_new_target(x, y)
                # self.setup_target(cu)
                # cu.update(dt)
                cu.state = "moving_to_entrance"

                # x, y = (self.wait_queue.pop())
                # cu.setup_new_target(x, y)
        

                # ログで確認
                logger.debug(f"【入り口でアサインする】id: {cu.id} pos: {x, y} state: {cu.state}")

                # 客の数をカウント
                self.count_num_customers += 1

                # pyglet.clock.schedule_once(lambda dt: self.moving_to_waiting_area(cu), 3)

        # cu.target_x = 17
        # cu.target_y = 2


    def move_to_entrance(self, dt):
        for cu in self.customers:
            if cu.state == "moving_to_entrance":
                cu.update(dt)
                if cu.reached:
                    cu.state = "arrive"
                    logger.debug(f"【入り口まで移動しました】id: {cu.id} pos: {cu.target_x, cu.target_y} state: {cu.state}")
                
                        
                        
                # self.chara_queue.put(cu)
                        
                # キャラのキューに追加
                # そのインスタンスをリストの中にいれて管理する
                # そのインスタンスをリストの中にいれて管理する
                # self.customers.append(cu)


    def assign_wait_area(self):
        for cu in self.customers:
            if cu.state == "arrive":
                # 最も近い人を待機場所に割り当てる
                for j, chaired in enumerate(self.wait_chair):
                    if not chaired:
                        self.wait_chair[j] = True
                        # 紐付けようのリストに入れる
                        self.waiting_queue.append((cu, j))
                        # self.wait_queue_j = self.wait_queue[j]
                        # target = self.wait_queue[j]
                        x, y = self.wait_queue[j]
                        y = self.real_grid_y - (y + 1)
                        cu.setup_new_target(x, y)

                        
                        # target = self.wait_queue[j]
                        # print(target)

                        # cu.setup_new_target(*target)
                        cu.state = "moving_to_wait"
                        logger.debug(f"【待機場所割当】id: {cu.id} index: W[{j}] pos: {x, y} \
                                state: {cu.state}")
                        

                        break
                        
                        

                # x, y = self.map.entrance_pos
                # y = self.real_grid_y - (y + 1)
                
                # x, y = self.wait_queue.get()
                # y = self.real_grid_y - (y + 1)
                # print(x, y)
                # print(self.wait_queue.get())
                # cu.setup_new_target(x, y)
                # self.setup_target(cu)
                # cu.update(dt)

                # x, y = (self.wait_queue.pop())
                # cu.setup_new_target(x, y)
        

                # ログで確認
                # self.log(f"【入り口でアサインする】pos: {x, y} state: {cu.state}")

                # pyglet.clock.schedule_once(lambda dt: self.moving_to_waiting_area(cu), 3)


                

    def moving_to_waiting_area(self, dt):
        for index, cu_waiting_queue in enumerate(self.waiting_queue):
            cu = cu_waiting_queue[0]
            if cu.state == "moving_to_wait":
                # print(f"{self.wait_queue}")
                x, y = (self.wait_queue[index])
                # print(f"元のxy{x, y}")
                cu.setup_new_target(x, y)
                cu.update(dt)
                

        # cu.state = "moving_to_wating_area"
        # # # x, y = self.wait_queue.get()
        # x, y = (self.wait_queue.pop())
        # # # y = self.real_grid_y - (y + 1)
        # cu.setup_new_target(x, y)
        # # print(x, y)
        

