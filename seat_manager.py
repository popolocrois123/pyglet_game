import pyglet
from loguru import logger


class SeatManager():
    def __init__(self, parent, map):
        self.parent = parent

        # mapデータの取得
        self.map = map

        # MAP上の座席の座標リスト
        self.seat_positions = self.map.seat_queue

        # 席管理のためのキュー
        # 1, 座席管理リスト
        self.seat_in_use = [False for i in range(len(self.seat_positions))]
        # 2, カスタマーのリストを取得
        self.customers = self.parent.customer_manager.customers
        for cu in self.customers:
            logger.info(f"{cu.reached}")
        # 3, 顧客と座席の紐づけ
        self.seat_queue = []

        # print(self.seat_in_use)

        # yの計算
        self.real_grid_y = len(self.map.map_data)




    def update(self, dt):
        # 客を席にセット
        self.assign_seat()

        # # 客を席に移動
        self.move_to_seat(dt)

        # # 客がごはんを食べる
        # self.eating()

        # # 客が出口まで移動する
        # self.move_to_exit


    def assign_seat(self):
        for cu in self.customers:
            if cu.state == "waiting_to_sit_to_seat":
                # waiting_queueの取得
                # self.waiting_queue = self.parent.customer_manager.waiting_queue
                # # 最も近い人を待機場所に割り当てる
                for j, in_use in enumerate(self.seat_in_use):
                    if not in_use:
                        self.seat_in_use[j] = True
                        x, y = self.seat_positions[j]
                        y = self.real_grid_y - (y + 1)
                        cu.setup_new_target(x, y)
                        cu.state = "moving_to_seat"
                        logger.debug(f"【席にアサインする】id: {cu.id}\
                        state: {cu.state}")
                        self.seat_queue.append((cu, j))

                        # wait_chairとwaiting_queueを変更する
                        # # logの確認
                        # logger.info(f"wait_chair: {self.parent.customer_manager.wait_chair}")
                        # logger.info(f"waiting_queue: {self.parent.customer_manager.waiting_queue}")
                        # self.parent.customer_manager.wait_chair[j] = False
                        logger.info(f"waiting_queue: {self.parent.customer_manager.waiting_queue}")
                        logger.info(f"waiting_queue: {self.parent.customer_manager.wait_chair}")

                        
                        # cuからwaiting_queueのcuに連結された番号を取り出す
                        for cu_value in self.parent.customer_manager.waiting_queue:
                            if cu in cu_value:
                                cu_number = cu_value[1]

                        # 番号に該当するwait_chairをFalseにすることで席を空席にする
                        self.parent.customer_manager.wait_chair[cu_number] = False
                        # wait_chair_num = self.parent.customer_manager.waiting_queue
                        
                        # waiting_queueからcuを取り出す 
                        self.parent.customer_manager.waiting_queue = [x for x in self.parent.customer_manager.waiting_queue if x[0] != cu]

                        logger.info(f"new waiting_queue: {self.parent.customer_manager.waiting_queue}")
                        logger.info(f"waiting_queue: {self.parent.customer_manager.wait_chair}")

                        # self.parent.customer_manager.waiting_queue.pop

                        # print(cu)

                        # logger.info(f"wait_chair: {self.parent.customer_manager.wait_chair}")
                        # logger.info(f"waiting_queue: {self.parent.customer_manager.waiting_queue}")

                        break
                # pass

        



    def move_to_seat(self, dt):
        for cu in self.customers:
            if cu.state == "moving_to_seat":
                cu.update(dt)

    def eating(self):
        pass

    def move_to_exit(self):
        pass