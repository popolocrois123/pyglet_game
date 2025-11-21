import pyglet
from setting import *
from loguru import logger

class SimpleMover:

    _id_counter = 0

    def __init__(self, start_pos, target_pos, state, map, batch):
        # 各顧客に一意のIDを付与
        self.id = SimpleMover._id_counter
        SimpleMover._id_counter += 1
        

        self.state = state
        self.map = map

        # 最初の出現場所の記録
        self.origin = "G"

        self.grid_x, self.grid_y = start_pos
        self.target_x, self.target_y = target_pos

        # self.real_grid_y = len(MAP_DATA) - self.grid_y - 1

        self.pixel_x = self.grid_x * CELL_SIZE
        self.pixel_y = self.grid_y * CELL_SIZE

        self.sprite_x = self.grid_x * CELL_SIZE
        self.sprite_y = self.grid_y * CELL_SIZE

        self.sprite = pyglet.shapes.Rectangle(
            x=self.pixel_x, y=self.pixel_y,
            width=CELL_SIZE, height=CELL_SIZE,
            color=(255, 0, 0),
            batch=batch
        )

        self.moving = False
        self.move_duration = 0.2  # 1マス移動にかかる時間（秒）
        self.move_timer = 0.0

        self.start_pixel = (self.pixel_x, self.pixel_y)
        self.dest_pixel = (self.pixel_x, self.pixel_y)

        # 元のMAD_DATAの保存
        self.MAP_DATA_COPY = MAP_DATA
        # print(self.MAP_DATA_COPY)

        # 到着判定フラグ
        self.reached = False

        self.count = 1

        # 退店処理
        self.stay_timer = 0.0


    # 目標値が定まった状態でその座標に移動開始する
    def start_move_to(self, new_x, new_y):
        self.start_pixel = (self.pixel_x, self.pixel_y)
        self.dest_pixel = (new_x * CELL_SIZE, new_y * CELL_SIZE)
        self.grid_x, self.grid_y = new_x, new_y
        self.move_timer = 0.0
        self.moving = True
    
    def update(self, dt):
        if self.moving:
            self.move_timer += dt
            t = min(self.move_timer / self.move_duration, 1.0)
            sx, sy = self.start_pixel
            dx, dy = self.dest_pixel
            self.pixel_x = sx + (dx - sx) * t
            self.pixel_y = sy + (dy - sy) * t

            self.sprite.x = self.pixel_x
            self.sprite.y = self.pixel_y



            if t >= 1.0:
                self.moving = False


        # 1マスの移動が完了している場合
        else:
            # 現在のグリッドがターゲットグリッドにまだ到達していない場合
            if (self.grid_x, self.grid_y) != (self.target_x, self.target_y):
                dx = self.target_x - self.grid_x
                dy = self.target_y - self.grid_y

                if dx != 0:
                    step_x = 1 if dx > 0 else -1
                    new_x = self.grid_x + step_x
                    new_y = self.grid_y


                elif dy != 0:
                    step_y = 1 if dy > 0 else -1
                    new_x = self.grid_x
                    new_y = self.grid_y + step_y


                self.start_move_to(new_x, new_y)
                
            else:
                # 既に目的地に到達
                self.reached = True
                return


    # MAP_DATAでキャラが動いた場所をCにする
    def change_map_to_chara(self):
        pass
    

    def return_map_to_origin_y(self, origin):
        pass
    
    # customer_managerから座標を受け取ってセットする
    def setup_new_target(self, x, y):
        self.target_x = x
        self.target_y = y

    


