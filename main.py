import pyglet
from pyglet.window import key
from model import Character, Hero
from map import Background, Map
from setting import *
import time
from collections import deque

class Main():
    def __init__(self):

        # lofファイルの読み込み
        log_path = "customer_lifecycle.log"
        
        # 客の動きを記録
        self.log_file = open(log_path, "w", encoding="utf-8")
        self.start_time = time.time()

        # ログ関数を作って渡す
        self.logger = Logger(log_path, max_logs=100)
        # self.log = self._create_logger()
    

        # 引数として渡されたwidthとheightを取り出す
        self.width = len(MAP_DATA[0]) * CELL_SIZE
        self.height = len(MAP_DATA) * CELL_SIZE

        # windowの設定
        self.window = pyglet.window.Window(width=self.width, height=self.height, caption="rpg", resizable=True)
        self.window.set_location(x=400, y=200)
        self.window.set_minimum_size(width=500, height=500)

        # キーを押している間だけ動く
        self.keys = key.KeyStateHandler()
        self.window.push_handlers(self.keys)
        
        # batchの作成
        self.batch = pyglet.graphics.Batch()

        # キャラクターのリスト
        self.characters = []


        self.logger.log("マップの読み込み開始")
        # 背景のmapクラスの呼び出し
        self.map = Map(MAP_DATA, CELL_SIZE, self.batch, self.height, log_func=self.logger.log)

        # 背景の呼び出し
        # self.background = Background(self.window, self.batch)

        # playerのスタート位置の呼び出し
        px, py = self.map.player_start

        # Heroクラスの呼び出し
        self.hero = Hero(px, py, self.window, self.batch, CELL_SIZE, self.map, self.keys, log_func=self.logger.log)
        self.characters.append(self.hero)

        # mainでデバッグを使う方法
        self.logger.log("mainの初期化完了しました。")

        
        # Heroの操作用
        self.window.push_handlers(self)

        pyglet.clock.schedule_interval(self.update, 1/30)

    # # デバッグ用
    # def _create_logger(self):
    #     def log(message: str):
    #         timestamp = round(time.time() - self.start_time, 2)
    #         self.log_file.write(f"[{timestamp}] {message}\n")
    #         self.log_file.flush()
    #     return log


    def on_draw(self):
        self.window.clear()
        self.batch.draw()
        # for chara in self.characters:
        #     chara.batch.draw()

    def update(self, dt: float):
        for chara in self.characters:
            chara.update(dt)


# ログを記録する
class Logger:
    def __init__(self, log_file_path, max_logs=100):
        self.log_file = open(log_file_path, "w", encoding="utf-8")
        self.start_time = time.time()
        self.max_logs = max_logs
        # 最大max_logsだけ保持
        self.log_buffer = deque(maxlen=max_logs)
    
    def log(self, message:str):
        timestamp = round(time.time() - self.start_time, 2)
        log_line = f"[{timestamp} {message}]"
        self.log_buffer.append(log_line)
        self.log_file.write(log_line + "\n")
        self.log_file.flush()

    def get_recent_logs(self):
        return list(self.log_buffer)
    
    def close(self):
        self.log_file.close()



if __name__ == "__main__":
    game = Main()
    pyglet.app.run()
