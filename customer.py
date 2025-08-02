import pyglet
from setting import *
import random

class Customer:
    def __init__(self, customer_mage, batch, window_width, window_height, log_func=None):
        # CustomerMageクラスの呼び出し
        self.customer_mage = customer_mage
        
        # 客の初期位置の座標（グリッド）
        self.initial_x, self.initial_y = self.customer_mage.initial_x, self.customer_mage.initial_y

        # ターゲット座標（グリッド）
        self.target_x, self.target_y = 17, 12

        # 定数
        self.window_width = window_width
        self.window_height = window_height
        # キャラクターの速度
        self.MOVE_SPEED = 100 # ピクセル/秒

        self.color = (255, 0, 0)

        # 客の画像
        self.sprite = pyglet.shapes.Rectangle(
            x=self.initial_x * CELL_SIZE,
            y=self.window_height - (self.initial_y + 1) * CELL_SIZE,
            width=CELL_SIZE,
            height=CELL_SIZE,
            color=self.color,
            batch=batch
        )

        # 移動用変数
        # 移動中の座標 0: x移動中、1: y移動中、　2:完了
        self.phase = 0
        self.from_x = self.sprite.x
        self.from_y = self.sprite.y
        self.to_x = self.target_x * CELL_SIZE
        self.to_y = self.window_height - (self.target_y + 1) * CELL_SIZE
        # 詠歌時間
        self.elapsed = 0
        # 4秒で移動する
        self.duration = 4

        self.log = log_func if log_func else lambda msg: None 
        self.count = 0
        self.log("Customerクラス初期化完了しました")


    def update(self, dt):
        if self.phase == 0:
            # 最初の1回目はdtが異常になることがあるので無視
            if self.elapsed == 0 and dt > 1.0:
                print("スキップ: 初期フレームが重すぎ")
                return
            self.elapsed += dt
            t = min(self.elapsed / self.duration, 1.0)
            new_x = self.from_x + (self.to_x - self.from_x) * t
            self.sprite.x = new_x
            print(f"[x移動] t={t: .2f}, x={new_x:.2f}]")
            if t >= 1.0:
                self.phase = 1
                # 経過時間をリセット
                # 現在のｙを保存
                self.elapsed = 0.0
                self.y_start_fixed = self.sprite.y

        elif self.phase == 1:
            self.elapsed += dt
            t = min(self.elapsed / self.duration, 1.0)
            new_y = self.from_y + (self.to_y - self.from_y) * t

            self.sprite.y = new_y
            print(f"[Y移動] t={t:.2f}, y={new_y:.2f}")
            if t >= 1.0:
                self.phase = 2
                print("移動完了")


class CustomerMage():
    def __init__(self):
        random_x = random.randint(1, 5)
        random_y = random.randint(1, 3)
        self.initial_x = random_x
        self.initial_y = random_y
        
        



        
    




