import pyglet
from pyglet.window import key
from model import Character, Hero
from map import Background, Map
from setting import *

class Main():
    def __init__(self):
        super().__init__()

        # 引数として渡されたwidthとheightを取り出す
        self.width = len(MAP_DATA[0]) * CELL_SIZE
        self.height = len(MAP_DATA) * CELL_SIZE
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
        
        # 背景のmapクラスの呼び出し
        self.map = Map(MAP_DATA, CELL_SIZE, self.batch, self.height)

        # 背景の呼び出し
        self.background = Background(self.window, self.batch)

        # Heroクラスの呼び出し
        self.hero = Hero(self.window, self.batch, self.keys, CELL_SIZE, self.height, self.map)
        self.characters.append(self.hero)

        
        # Heroの操作用
        self.window.push_handlers(self)

        pyglet.clock.schedule_interval(self.update, 1/60)

        

    def on_draw(self):
        self.window.clear()
        self.batch.draw()
        # for chara in self.characters:
        #     chara.batch.draw()

    def update(self, dt: float):
        for chara in self.characters:
            chara.update(dt)


if __name__ == "__main__":
    # window = Main(width=500, height=600, caption="ball", resizable=True)
    # pyglet.clock.schedule_interval(window.update, 1/60)
    game = Main()
    pyglet.app.run()
