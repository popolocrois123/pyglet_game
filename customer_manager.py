from customer import Customer
import time
import pyglet
from simple_mover import SimpleMover
import random
import queue
from loguru import logger

class CustomerManager:
    def __init__(self, parent, map_data, map, num_customers=10):
        self.parent = parent

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
        # logger.debug(f"待機場所の座標{self.wait_queue}")

        # 入り口のキュー（エントランスと待合室のマックスの人数）
        self.max_entrance_buffer = len(self.wait_queue) + 1

        # 現在の入り口キューへの客入りの状況
        self.current_entrance_buffer = 0

        # 顧客の入口での管理のためのキュー
        # 1, 待機場所管理リスト
        self.wait_chair = [False for i in range(len(self.wait_queue))]
        # print(self.wait_chair)
        # 2, 顧客本体のリスト
        self.customers = []
        # 3, 顧客と待機場所の紐づけ
        self.waiting_queue = []

        # 待機場所が使われているかどうかのリスト
        # [宿題]
        self.wait_pos_in_use = [False] * len(self.wait_chair)
        # 新規顧客の生成
        self.spawn_timer = 0.0
        self.spawn_interval = 20 # 5秒ごとに新しい顧客を生成
        # self.max_customers = 7   # 任意：上限を設定したい場合
        self.max_customers = 20  # 任意：上限を設定したい場合
        # logger.debug(f"max_customer: {self.max_customers}")

        # 初期顧客
        self.setup_initial_customers()

        # 客のターゲット座標のリスト
        self.target_list = []

        self.count = 1

    # 初期顧客の生成
    def setup_initial_customers(self):
        # ⭐ 初期顧客を spawn_customer() 経由で生成
        for _ in range(self.num_customers_to_initialize):
            # もし客（self.count_num_customers）がself.max_customersより小さかったら
            if self.count_num_customers < self.max_customers:
                self.spawn_customer()
                self.count_num_customers += 1

    def update(self, dt):
        # 入口まで割り当て
        self.assign_entrance()

        # 入口まで移動
        self.move_to_entrance(dt)

        # 待機場所への割り当て
        self.assign_wait_area()

        # 待機場所への移動
        self.moving_to_waiting_area(dt)

        # 客の削除
        self.delete_customer(dt)

        # 宿題
        # ループさせる
        # # self.setup_initial_customers()
        self.spawn_customer()


    # 顧客生成
    def spawn_customer(self):
        if self.count_num_customers < self.max_customers:

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
                                        batch=self.batch)

            # # そのインスタンスをリストの中にいれて管理する
            self.customers.append(simple_mover)

            # 宿題
            self.count_num_customers += 1



    # 入り口までアサインする（受付）
    def assign_entrance(self):
        for cu in self.customers:
            if cu.state == "outside":
                if self.current_entrance_buffer <= self.max_entrance_buffer:
                    x, y = self.map.entrance_pos
                    # logger.debug(f"入り口の目標座標の確認（変更前）{x,y} 高さ{len(self.map_data)}")
                    x, y = self.map.to_pyglet_x_y(x, y)
                    # logger.debug(f"入り口の目標座標の確認（変更後）{x,y} 高さ{len(self.map_data)}")
                    # y = self.real_grid_y - (y + 1)
                    cu.setup_new_target(x, y)
                    cu.state = "moving_to_entrance"


                    # ログで確認
                    # logger.debug(f"【入り口でアサインする】id: {cu.id} pos: {x, y} state: {cu.state}")

                    # 客の数をカウント
                    # self.count_num_customers += 1

                    self.current_entrance_buffer += 1

                    # # [宿題]色を変える: 緑に
                    # cu.sprite.color=(0, 255, 0)



    def move_to_entrance(self, dt):
        for cu in self.customers:
            if cu.state == "moving_to_entrance":
                cu.update(dt)
                if cu.reached:
                    cu.state = "arrive"
                    cu.reached = False

                    # 宿題
                    # # 客の数を減らす
                    self.count_num_customers -= 1


    def assign_wait_area(self):
        for cu in self.customers:
            if cu.state == "arrive":
                # 最も近い人を待機場所に割り当てる
                # logger.debug(f"{self.wait_chair}")
                for j, chaired in enumerate(self.wait_chair):
                    if not chaired:
                        self.wait_chair[j] = True
                        
                        # 紐付けようのリストに入れる
                        self.waiting_queue.append((cu, j))

                        x, y = self.wait_queue[j]
                        x, y = self.map.to_pyglet_x_y(x, y)

                        cu.state = "moving_to_wait"                      
                        break

                

    def moving_to_waiting_area(self, dt):
        for index, cu_waiting_queue in enumerate(self.waiting_queue):
            cu = cu_waiting_queue[0]
            # logger.debug(f"{cu.grid_x, cu.grid_y}")
            if cu.state == "moving_to_wait":
                x, y = (self.wait_queue[index])
                x, y = self.map.to_pyglet_x_y(x, y)
                cu.setup_new_target(x, y)
                cu.update(dt)

                if cu.reached:
                    if index == 0:
                        cu.state = "waiting_to_sit_to_seat"
                        
                        # logger.info(f"【待機場所に到着】id: {cu.id} pos: {cu.grid_x, cu.grid_y} \
                        #                 state: {cu.state}")
                    # else:
                    #     cu.state = "waiting_for_top"
                    cu.reached = False
                


    # 客が削除される
    def delete_customer(self, dt):
        for i, cu in enumerate(self.customers):
            # logger.info(f"state: {cu.state}")
            if cu.state == "exited":
                logger.info(f"state: {cu.state}")
                # # そのインスタンスをリストの中にいれて管理する
                
                # 明示的にスプライトを削除
                if hasattr(cu, 'sprite') and cu.sprite:
                    cu.sprite.delete()

                self.customers.pop(i)

                # # 宿題
                # # # 客の数を減らす
                # self.count_num_customers -= 1
                # # # self.setup_initial_customers()
                # # self.update(dt)
                # if self.count_num_customers < self.max_customers:
                #     self.spawn_customer()
                #     self.count_num_customers += 1


    def chack_waiting(self):
        pass

    # 詰める処理
    def shift_waiting_customers_forward(self):
        for i in range(len(self.wait_chair)):
            if not self.wait_chair[i]:
                # 後の顧客を詰める
                for id, (customer, current_i) in enumerate(self.waiting_queue):
                    # もし、紐付けられた座席が昇順の座席よりも大きい値ならば、一致させる
                    if id > i:
                        # idにいる客をiに移動
                        self.waiting_queue[id] = (customer, i)
                        # wait_chairのidの座席をFalseにしてiをTrueにする
                        self.wait_chair[id] = False
                        self.wait_chair[i] = True
                        # x, y = (self.waiting_queue[id])
                        # customer.setup_new_target(x, y)
                        customer.state = "moving_to_wait"
                        break
