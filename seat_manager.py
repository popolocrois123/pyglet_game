import pyglet
from loguru import logger
from setting import *

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
            logger.debug(f"{cu.reached}")
        # 3, 顧客と座席の紐づけ
        self.seat_queue = []

        # print(self.seat_in_use)

        # yの計算
        self.real_grid_y = len(self.map.map_data)

        # 席について食べているか、動き始めるかの判定
        self.start_to_exit = False



    def update(self, dt):
        # 客を席にセット
        self.assign_seat()

        # # 客を席に移動
        self.move_to_seat(dt)

        # 客がごはんを食べる
        self.eating(dt)

        # 客が出口まで移動する
        self.move_to_exit(dt)


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
                        # logger.debug(f"wait_chair: {self.parent.customer_manager.wait_chair}")
                        # logger.debug(f"waiting_queue: {self.parent.customer_manager.waiting_queue}")
                        # self.parent.customer_manager.wait_chair[j] = False
                        # logger.debug(f"waiting_queue: {self.parent.customer_manager.waiting_queue}")
                        # logger.debug(f"waiting_queue: {self.parent.customer_manager.wait_chair}")
                        # logger.debug(f"waiting_queue: {len()}")
                        
                        
                        # cuからwaiting_queueのcuに連結された番号を取り出す
                        for cu_value in self.parent.customer_manager.waiting_queue:
                            if cu in cu_value:
                                cu_number = cu_value[1]

                        # 番号に該当するwait_chairをFalseにすることで席を空席にする
                        self.parent.customer_manager.wait_chair[cu_number] = False
                        # wait_chair_num = self.parent.customer_manager.waiting_queue
                        
                        # waiting_queueからcuを取り出す 
                        self.parent.customer_manager.waiting_queue = [x for x in self.parent.customer_manager.waiting_queue if x[0] != cu]

                        # logger.debug(f"new waiting_queue: {self.parent.customer_manager.waiting_queue}")
                        # logger.debug(f"waiting_queue: {self.parent.customer_manager.wait_chair}")
                        logger.debug(f"wait_queue: {self.parent.customer_manager.wait_queue}")


                        # self.parent.customer_manager.waiting_queue.pop

                        # print(cu)

                        # logger.debug(f"wait_chair: {self.parent.customer_manager.wait_chair}")
                        # logger.debug(f"waiting_queue: {self.parent.customer_manager.waiting_queue}")

                        self.parent.customer_manager.current_entrance_buffer -= 1

                        break
                # pass

        



    def move_to_seat(self, dt):
        for cu in self.customers:
            if cu.state == "moving_to_seat":
                cu.update(dt)
                if cu.reached:
                    cu.state = "seated"
                    cu.reached = False
                # cu.state = "seated"
                logger.debug(f"【席につく】id: {cu.id}\
                        state: {cu.state}")
    

    def eating(self, dt):
        for cu in self.customers:
            if cu.state == "seated":
                cu.stay_timer += dt
                if cu.stay_timer >= STAY_DURATION:
                    x, y = self.map.exit_pos
                    y = self.real_grid_y - (y + 1)
                    cu.setup_new_target(x, y)
                    # [宿題]色を変える: 緑に
                    cu.sprite.color=(0, 255, 0)

                    cu.state = "leaving"
    #             # 3秒後に enable_move を呼び出す
    #             pyglet.clock.schedule_once(cu.update, 10.0)
    #             # if self.start_to_exit == False:
    #             #     # 3秒後に enable_move を呼び出す
    #             #     pyglet.clock.schedule_once(cu.update, 10.0)
    #             #     self.start_to_exit = True
    #             logger.debug(f"【食事中】id: {cu.id}\
    #                     state: {cu.state}")
    #             break


    def move_to_exit(self, dt):
        for cu in self.customers:
            if cu.state == "leaving":
                cu.update(dt)
                if cu.reached:
                    cu.state = "exited"