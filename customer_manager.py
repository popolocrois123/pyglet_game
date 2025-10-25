from customer import Customer
import time
import pyglet
from simple_mover import SimpleMover
import random
import queue
from loguru import logger

class CustomerManager:
    def __init__(self, parent, map_data, map, num_customers=1, log_func=None):
        self.parent = parent
        self.log = log_func if log_func else lambda msg: None  # ログがなければ無効化

        self.batch = self.parent.batch

        # map_dataの取得
        self.map_data = map_data

        # mapクラスの呼び出し
        self.map = map

        # yの計算
        self.real_grid_y = len(self.map_data)

        # ランダムエリアを取得
        self.general_area = self.parent.map.general_costomer_area
        
        # 初期顧客数
        self.num_customers_to_initialize = num_customers

        # 現在の客の数の管理
        self.count_num_customers = 0

        # mapのWの場所のリストを取得
        self.wait_queue = self.map.wait_queue
        logger.info(f"待機場所の座標{self.wait_queue}")

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

        self.count = 1

    # 初期顧客の生成
    def setup_initial_customers(self):
        # ⭐ 初期顧客を spawn_customer() 経由で生成
        for _ in range(self.num_customers_to_initialize):
            self.spawn_customer()

    def update(self, dt):
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
        x, y = random_G
        x, y = self.map.to_pyglet_x_y(x, y)

        grid = (x, y)

        # 状態を決める
        # 顧客生成(店外)
        state = "outside"

        # 生成する直後は動かないのでスタート位置とゴール位置を同じにする
        simple_mover = SimpleMover(grid, grid,
                                    state, self.map,
                                    batch=self.batch,
                                    log_func=self.log)

        # # そのインスタンスをリストの中にいれて管理する
        self.customers.append(simple_mover)

        # ログで確認
        logger.debug(f"【顧客生成】id: {simple_mover.id} pos: {random_G} state: {state}")
        

    # 入り口までアサインする（受付）
    def assign_entrance(self):
        for cu in self.customers:
            if (cu.state == "outside") and (self.count_num_customers <= self.max_customers):
                logger.info(f"self.customersの座標の確認assign_entrance {cu.grid_x, cu.grid_y}")

                x, y = self.map.entrance_pos
                logger.info(f"入り口の目標座標の確認（変更前）{x,y} 高さ{len(self.map_data)}")
                x, y = self.map.to_pyglet_x_y(x, y)
                logger.info(f"入り口の目標座標の確認（変更後）{x,y} 高さ{len(self.map_data)}")
                # y = self.real_grid_y - (y + 1)
                cu.setup_new_target(x, y)
                cu.state = "moving_to_entrance"


                # ログで確認
                # logger.debug(f"【入り口でアサインする】id: {cu.id} pos: {x, y} state: {cu.state}")

                # 客の数をカウント
                self.count_num_customers += 1


    def move_to_entrance(self, dt):
        for cu in self.customers:
            if cu.state == "moving_to_entrance":
                cu.update(dt)
                if cu.reached:
                    cu.state = "arrive"
                    # logger.debug(f"【入り口まで移動しました】id: {cu.id} pos: {cu.target_x, cu.target_y} state: {cu.state}")
                    
                    logger.info(f"self.customersの座標の確認move_to_entrance {cu.grid_x, cu.grid_y}")



    def assign_wait_area(self):
        for cu in self.customers:
            # logger.info(f"self.customesから呼び出した客の座標{cu.grid_x, cu.grid_y}")
            if cu.state == "arrive":
                # 最も近い人を待機場所に割り当てる
                logger.info(f"{self.wait_chair}")
                for j, chaired in enumerate(self.wait_chair):
                    if not chaired:
                        self.wait_chair[j] = True
                        
                        # 紐付けようのリストに入れる
                        self.waiting_queue.append((cu, j))
                        # logger.info(f"waiting_queueの一つの座標{self.waiting_queue[j][0].grid_x, self.waiting_queue[j][0].grid_y}")

                        # self.wait_queue_j = self.wait_queue[j]
                        # target = self.wait_queue[j]
                        # x, y = self.wait_queue[j]
                        # x, y = self.map.entrance_pos
                        logger.info(f"wait_queueの一つの座標の確認1{x,y} 高さ{len(self.map_data)}")
                        logger.info(f"wait_queueの座標{self.wait_queue}")
                        # logger.info(f"wait_queueの確認（変更前）{self.wait_queue} 高さ{len(self.map_data)}")

                        # y = self.real_grid_y - (y + 1)
                        x, y = self.map.to_pyglet_x_y(x, y)
                        # logger.info(f"待機場所への割り当ての座標{x, y}")
                        logger.info(f"wait_queueの確認（変更後）{x, y}")
                        logger.info(f"self.customersの座標の確認assign_wait_area {cu.grid_x, cu.grid_y}")
                        
                        # cu.setup_new_target(x, y)

                        # cu.setup_new_target(*target)
                        cu.state = "moving_to_wait"
                        # logger.debug(f"【待機場所割当】id: {cu.id} index: W[{j}] pos: {x, y} \
                        #         state: {cu.state}")
                        

                        break

                

    def moving_to_waiting_area(self, dt):
        for index, cu_waiting_queue in enumerate(self.waiting_queue):
            cu = cu_waiting_queue[0]
            # logger.info(f"{cu.grid_x, cu.grid_y}")
            if cu.state == "moving_to_wait":
                # print(f"{len(self.waiting_queue)}")
                x, y = (self.wait_queue[index])
                # logger.info(f"変更前のｘｙ{x, y}")
                # x, y = self.map.to_pyglet_x_y(x, y)
                # logger.info(f"変更後のｘｙ{x, y}")
                # print(f"元のxy{x, y}")
                cu.setup_new_target(x, y)
                cu.update(dt)
                # if self.count == 1:
                #     logger.info(f"{cu.target_x, cu.target_y}")
                #     self.count = 2
                if cu.grid_x == cu.target_x and cu.grid_y == cu.target_y:
                # logger.info(f"{cu.grid_x, cu.grid_y}")
                # if cu.reached:
                    cu.state = "waiting_to_sit_to_seat"
                    # logger.debug(f"【待機場所に到着】id: {cu.id} pos: {cu.grid_x, cu.grid_y} \
                    #                 state: {cu.state}")
                # #     break

    # 客が削除される
    def delete_customer(self):
        pass

    def chack_waiting(self):
        # for index, cu_waiting_queue in enumerate(self.waiting_queue):
        #     cu = cu_waiting_queue[0]
        pass