import pyglet
from model import Character, Hero

class Main(pyglet.window.Window):
    def __init__(self, width, height, caption, resizable):
        super().__init__(width, height, caption, resizable)

        # 引数として渡されたwidthとheightを取り出す
        self.width = width
        self.height = height

        self.set_location(x=400, y=200)
        self.set_minimum_size(width=500, height=500)
        
        # # Modelクラスの呼び出し
        # self.character = Character(self)

        # キャラクターのリスト
        self.characters = []

        # Heroクラスの呼び出し
        self.hero = Hero(self)
        self.characters.append(self.hero)

        # Heroの操作用
        self.push_handlers(self.hero)

        

    def on_draw(self):
        self.clear()
        for chara in self.characters:
            chara.batch.draw()

    def update(self, dt: float):
        for chara in self.characters:
            chara.update(dt)


if __name__ == "__main__":
    window = Main(width=500, height=400, caption="ball", resizable=True)
    pyglet.clock.schedule_interval(window.update, 1/60)
    pyglet.app.run()
