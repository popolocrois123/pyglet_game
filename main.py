import pyglet
from pyglet.window import key
# from model import Character, Hero
from map import Background, Map
from setting import *
from logger import Logger
import time
from customer import Customer
from customer_manager import CustomerManager


class Main():
    def __init__(self):
        
        # 客の動きを記録
        self.log_file = open(LOG_PATH, "w", encoding="utf-8")
        self.start_time = time.time()

        # ログ関数を作って渡す
        self.logger = Logger(LOG_PATH, max_logs=MAX_LOGS)
        # self.log = self._create_logger()
    

        # 引数として渡されたwidthとheightを取り出す
        self.width = len(MAP_DATA[0]) * CELL_SIZE
        self.height = len(MAP_DATA) * CELL_SIZE

        # windowの設定
        self.window = pyglet.window.Window(width=self.width, height=self.height,
                                            caption="rpg", resizable=True)
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
        self.map = Map(MAP_DATA, CELL_SIZE, self.batch, self.height, 
                       log_func=self.logger.log)

        # 背景の呼び出し
        # self.background = Background(self.window, self.batch)

        # # playerのスタート位置の呼び出し
        # px, py = self.map.player_start

        # CustomerMageクラスの呼び出し
        self.customer_manager = CustomerManager(self, MAP_DATA, self.map,
                                log_func=self.logger.log)

        # Heroクラスの呼び出し
        # self.hero = Hero(px, py, self.window, self.batch, CELL_SIZE, self.map, self.keys, log_func=self.logger.log)
        # ここに入れる
        # self.simple_mover = SimpleMover((1, 1), (10, 1), 
        #                                 batch=self.batch,
        #                                 log_func=self.logger.log)
        # self.customer = Customer(self.customer_manager,
        #                     batch=self.batch,
        #                     window_width=self.width,
        #                     window_height=self.height,
        #                     log_func=self.logger.log,
        #                     )
        # self.characters.append(self.customer)


        # mainでデバッグを使う方法
        self.logger.log("mainの初期化完了しました。")

        
        # Heroの操作用
        self.window.push_handlers(self)

        pyglet.clock.schedule_interval(self.update, 1/30)


    def on_draw(self):
        self.window.clear()
        self.batch.draw()
        # for chara in self.characters:
        #     chara.batch.draw()

    def update(self, dt: float):
        # self.customer.update(dt)
        # self.simple_mover.update(dt)
        self.customer_manager.update(dt)

        # for chara in self.characters:
        #     chara.update(dt)


if __name__ == "__main__":
    game = Main()
    pyglet.app.run()
