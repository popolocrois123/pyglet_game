import pyglet
from setting import *

class SimpleMover:
    def __init__(self, start_pos, target_pos, state, batch, log_func=None):
        self.log = log_func if log_func else lambda msg: None  # ログがなければ無効化

        self.state = state
        self.grid_x, self.grid_y = start_pos
        self.target_x, self.target_y = target_pos

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
        self.log(f"{self.pixel_x}: {self.pixel_y}")


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
            self.log(f"{self.pixel_x}: {self.pixel_y}")


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
                else:
                    # 既に目的地に到達
                    return

                self.start_move_to(new_x, new_y)


